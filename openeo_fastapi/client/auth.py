import datetime
import uuid
from abc import ABC, abstractmethod
from enum import Enum

import requests
from fastapi import Header
from pydantic import BaseModel, Field, ValidationError, validator

from openeo_fastapi.client.exceptions import (
    InvalidIssuerConfig,
    TokenCantBeValidated,
    TokenInvalid,
)
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

    @classmethod
    def get_orm(cls):
        return UserORM

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = "ignore"


class Authenticator(ABC):
    # Authenticator validate method needs to know what decisions to make based on user info response from the issuer handler.
    # This will be different for different backends, so just put it as ABC for now. We might be able to define this if we want
    # to specify an auth config when initialising the backend.
    @abstractmethod
    def validate(authorization: str = Header()):
        settings = AppSettings()

        issuer = IssuerHandler(
            issuer_url=settings.OIDC_URL,
            organisation=settings.OIDC_ORGANISATION,
            roles=settings.OIDC_ROLES,
        )

        user_info = issuer.validate_token(authorization)

        found_user = get_first_or_default(
            User, Filter(column_name="oidc_sub", value=user_info.info["sub"])
        )

        if found_user:
            return found_user

        user = User(user_id=uuid.uuid4(), oidc_sub=user_info.info["sub"])
        create(user)
        return user


class AuthMethod(Enum):
    """Enum defining known auth methods."""

    BASIC = "basic"
    OIDC = "oidc"


# Breaks the OpenEO token format down into it's components. This makes it possible to use the token against the issuer.
class AuthToken(BaseModel):
    """ """

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


# TODO Remove? Would be good to generate the user info model for each issuer that is provided.
class UserInfo(BaseModel):
    """ """

    info: dict


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
        """ """
        return requests.get(self.issuer_url + OIDC_WELLKNOWN_CONFIG_PATH)

    def _get_user_info(self, info_endpoint, token):
        """ """
        return requests.get(
            info_endpoint,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

    def _validate_oidc_token(self, token: str) -> UserInfo:
        """ """

        issuer_oidc_config = self._get_issuer_config()

        if issuer_oidc_config.status_code != 200:
            raise InvalidIssuerConfig()

        userinfo_url = issuer_oidc_config.json()[OIDC_USERINFO]
        resp = self._get_user_info(userinfo_url, token)

        if resp.status_code != 200:
            raise TokenInvalid()

        return UserInfo(info=resp.json())

    def validate_token(self, token: str) -> UserInfo:
        """Try to validate the token against the give OIDC provider."""
        # TODO Handle validation exceptions
        parsed_token = AuthToken.from_token(token)

        if parsed_token.method.value == AuthMethod.OIDC.value:
            return self._validate_oidc_token(parsed_token.token)
        raise TokenCantBeValidated()
