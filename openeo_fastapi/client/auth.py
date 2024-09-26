"""Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - User: Framework for defining and extending the logic for working with BatchJobs.
    - Authenticator: Class holding the abstract validation method used for authentication for API endpoints.
    - AuthMethod: Enum defining the available auth methods.
    - AuthToken: Pydantic model for breaking and validating an OpenEO Token into it's consituent parts.
    - IssuerHandler: Class for handling the AuthToken and validating against the revelant token Issuer and AuthMethod.
"""
import datetime
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import requests
from fastapi import Header, HTTPException
from jose import jwt
from pydantic import BaseModel, ValidationError, validator

from openeo_fastapi.api.types import Error
from openeo_fastapi.client.psql.engine import Filter, create, get_first_or_default
from openeo_fastapi.client.psql.models import UserORM
from openeo_fastapi.client.settings import AppSettings

ALGORITHMS = ["RS256"]
OIDC_WELLKNOWN_CONFIG_PATH = "/.well-known/openid-configuration"
OIDC_USERINFO = "userinfo_endpoint"
OIDC_JWKS = "jwks_uri"


class User(BaseModel):
    """Pydantic model manipulating users."""

    user_id: uuid.UUID
    oidc_sub: str
    created_at: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        """Pydantic model class config."""

        orm_mode = True
        arbitrary_types_allowed = True
        extra = "ignore"

    @classmethod
    def get_orm(cls):
        """Get the ORM model for this pydantic model."""
        return UserORM


# TODO Might make more sense to merge with IssueHandler class.
# TODO The validate function needs to be easier to overwrite and inject into the OpenEO Core client.
class Authenticator(ABC):
    """Basic class to hold the validation call to be used by the api endpoints requiring authentication."""

    # Authenticator validate method needs to know what decisions to make based on user info response from the issuer handler.
    # This will be different for different backends, so just put it as ABC for now. We might be able to define this if we want
    # to specify an auth config when initialising the backend.
    @abstractmethod
    def validate(authorization: str = Header()):
        """Validate the authorisation header and create a new user. This method can be overwritten as needed.

        Args:
            authorization (str): The authorisation header content from the request headers.

        Returns:
            User: The authenticated user.
        """
        settings = AppSettings()

        policies = None
        if settings.OIDC_POLICIES:
            policies = settings.OIDC_POLICIES
        issuer = IssuerHandler(issuer_uri=settings.OIDC_URL, policies=policies)

        user_info = issuer.validate_token(authorization)

        found_user = get_first_or_default(
            User, Filter(column_name="oidc_sub", value=user_info["sub"])
        )

        if found_user:
            return found_user

        user = User(user_id=uuid.uuid4(), oidc_sub=user_info["sub"])

        create(create_object=user)
        return user


class AuthMethod(Enum):
    """Enum defining known auth methods."""

    BASIC = "basic"
    OIDC = "oidc"


# Breaks the OpenEO token format down into it's components. This makes it possible to use the token against the issuer.
class AuthToken(BaseModel):
    """The AuthToken breaks down the OpenEO token into its consituent parts to be used for validation."""

    method: AuthMethod
    provider: str
    token: str

    @validator("provider", pre=True)
    def check_provider(cls, v, values, **kwargs):
        if v == "":
            raise ValidationError("Empty provider string.")
        return v

    @validator("token", pre=True)
    def check_token(cls, v, values, **kwargs):
        if v == "":
            raise ValidationError("Empty token string.")
        return v

    @classmethod
    def from_token(cls, token: str):
        """Takes the openeo format token, splits it into the component parts, and returns an Auth token."""

        if "Bearer " in token:
            token = token.removeprefix("Bearer ")

        return cls(**dict(zip(["method", "provider", "token"], token.split("/"))))


class IssuerHandler(BaseModel):
    """General token handler for querying provided tokens against issuers."""

    issuer_uri: str
    policies: list[str] = None

    @validator("issuer_uri", pre=True)
    def remove_trailing_slash(cls, v, values, **kwargs):
        if v.endswith("/"):
            return v.removesuffix("/")
        return v

    def _get_issuer_config(self):
        """Get the well known config of the issuer url.

        Returns:
            Direct response object from the request.
        """
        return requests.get(self.issuer_uri + OIDC_WELLKNOWN_CONFIG_PATH)

    def _get_user_info(self, info_endpoint, token):
        """Get the user info from  known config of the issuer url.

        Args:
            info_endpoint (str): The url of the user info endpoint to request.
            token (str): The token to be used as the bearer token in the authorization header.

        Returns:
            Direct response object from the request.
        """
        return requests.get(
            info_endpoint,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

    def _get_oidc_jwks(self, issuer_config):
        """Get the jwks uri from the issuer config.

        Args:
            issuer_config (dict): The url of the user info endpoint to request.

        Returns:
            Direct response object from the request.
        """
        jwks_uri = issuer_config.json()[OIDC_JWKS]
        return requests.get(jwks_uri)

    def _validate_token(self, token, jwks):
        """Ensure the token is valid by verifying the token using the jwts of the issuer.

        Args:
            token (str): The token to be checked.
            jwks (dict): The jwks from the issuer.

        Returns:
            Payload (dict): True represents a valid token, False invalid..
        """
        # Decode the JWT token without validation to extract the header
        unverified_header = jwt.get_unverified_header(token)

        # Find the correct key to verify the token signature
        rsa_key = {}
        for key in jwks:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break
        if rsa_key:
            # Validate the token and verify claims
            payload = jwt.decode(
                token, rsa_key, algorithms=ALGORITHMS, issuer=self.issuer_uri
            )
            return payload

    def _authenticate_oidc_user(self, token: str):
        """Validate the provided oidc token against the oidc provider.

        Args:
            token (str): The token to be used as the bearer token in the authorization header.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            JSON from the response object from the request.
        """

        issuer_oidc_config = self._get_issuer_config()

        if issuer_oidc_config.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=Error(
                    code="InvalidIssuerConfig",
                    message="The issuer config is not available. Tokens cannot be validated currently. Try again later.",
                ),
            )

        jwks_resp = self._get_oidc_jwks(issuer_oidc_config)

        if issuer_oidc_config.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=Error(
                    code="InvalidIssuerConfig",
                    message=f"Key: jwks_uri is not available at the oidc config {OIDC_WELLKNOWN_CONFIG_PATH} location.",
                ),
            )

        jwks = jwks_resp.json()["keys"]

        if self._validate_token(token, jwks):
            # We can see if the user can be authenticated.
            userinfo_uri = issuer_oidc_config.json()[OIDC_USERINFO]

            resp = self._get_user_info(userinfo_uri, token)
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=Error(
                        code="InvalidIssuerConfig",
                        message=f"Key: {OIDC_USERINFO} is not available at the oidc config {OIDC_WELLKNOWN_CONFIG_PATH} location.",
                    ),
                )

            userinfo = resp.json()

            # If policies have been set for this provider, only allow users who match.
            if self.policies:
                for policy in self.policies:
                    key, value = policy.split(",")

                    for info in userinfo[key]:
                        if info == value:
                            return userinfo

                raise HTTPException(
                    status_code=500,
                    detail=Error(
                        code="TokenInvalid",
                        message=f"No existing access policy applies to user. Contact backend provider.",
                    ),
                )

            return userinfo

        raise HTTPException(
            status_code=500,
            detail=Error(
                code="TokenInvalid", message=f"The provided token is not valid."
            ),
        )

    def validate_token(self, token: str):
        """Try to validate the token against the give OIDC provider.

        Args:
            token (str): The OpenEO token to be parsed and validated against the oidc provider.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            The JSON as dictionary from _validate_oidc_token.
        """
        # TODO Handle validation exceptions
        parsed_token = AuthToken.from_token(token)

        if parsed_token.method.value == AuthMethod.OIDC.value:
            return self._authenticate_oidc_user(parsed_token.token)

        raise HTTPException(
            status_code=500,
            detail=Error(
                code="TokenCantBeValidated",
                message=f"The provided token cannot be validated.",
            ),
        )
