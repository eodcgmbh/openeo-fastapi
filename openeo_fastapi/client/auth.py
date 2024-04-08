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

import requests
from fastapi import Header, HTTPException
from pydantic import BaseModel, ValidationError, validator

from openeo_fastapi.api.types import Error
from openeo_fastapi.client.psql.engine import Filter, create, get_first_or_default
from openeo_fastapi.client.psql.models import UserORM
from openeo_fastapi.client.settings import AppSettings

OIDC_WELLKNOWN_CONFIG_PATH = "/.well-known/openid-configuration"
OIDC_USERINFO = "userinfo_endpoint"


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
    """Basic class to hold the validation call to be used by the api endpoints requiring authentication.
    """
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

        issuer = IssuerHandler(
            issuer_url=settings.OIDC_URL,
            organisation=settings.OIDC_ORGANISATION,
            roles=settings.OIDC_ROLES,
        )

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

    bearer: bool
    method: AuthMethod
    provider: str
    token: str

    @validator("bearer", pre=True)
    def passwords_match(cls, v, values, **kwargs):
        if v != "Bearer ":
            return ValueError("Token not formatted correctly")
        return True

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
        return cls(
            **dict(zip(["bearer", "method", "provider", "token"], token.split("/")))
        )


class IssuerHandler(BaseModel):
    """General token handler for querying provided tokens against issuers."""

    issuer_url: str
    organisation: str
    # TODO Roles will need to be used by the Authenticator class to be checked against the user info.
    roles: list

    @validator("issuer_url", pre=True)
    def remove_trailing_slash(cls, v, values, **kwargs):
        if v.endswith("/"):
            return v.removesuffix("/")
        return v

    def _get_issuer_config(self):
        """Get the well known config of the issuer url.

        Returns:
            Direct response object from the request.
        """
        return requests.get(self.issuer_url + OIDC_WELLKNOWN_CONFIG_PATH)

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

    def _validate_oidc_token(self, token: str):
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
                detail=Error(code="InvalidIssuerConfig", message=f"The issuer config is not available. Tokens cannot be validated currently. Try again later."),
            )

        userinfo_url = issuer_oidc_config.json()[OIDC_USERINFO]
        resp = self._get_user_info(userinfo_url, token)

        if resp.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=Error(code="TokenInvalid", message=f"The provided token is not valid."),
            )

        return resp.json()

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
            return self._validate_oidc_token(parsed_token.token)
        
        raise HTTPException(
            status_code=500,
            detail=Error(code="TokenCantBeValidated", message=f"The provided token cannot be validated."),
        )
