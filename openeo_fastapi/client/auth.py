from enum import Enum
from pathlib import Path

import requests
from pydantic import BaseModel, validator


# TODO Needs to be set for endpoints when registering
class AuthMethod(Enum):
    """Enum defining known auth methods."""

    BASIC = "basic"
    OIDC = "oidc"


class AuthProvider(Enum):
    """Enum defining known oidc providers."""

    EGI = "egi"
    NONE = ""


class AuthToken(BaseModel):
    """ """

    bearer: bool
    method: str
    provider: AuthProvider
    token: str

    @validator("bearer", pre=True)
    def passwords_match(cls, v, values, **kwargs):
        if v != "Bearer ":
            return ValueError("Token not formatted correctly")
        return True


# TODO Maybe remove the exceptions, and userinfo
class TokenInvalid(Exception):
    """ """

    pass


class TokenNotValidated(Exception):
    """ """

    pass


class UserInfo(BaseModel):
    """ """

    info: dict


class TokenHandler(BaseModel):
    """General token handler for querying provided tokens against issuers."""

    issuer_url: str
    organisation: str
    roles: list

    def _validate_oidc_token(self, token: str) -> UserInfo:
        """ """

        issuer_oidc_config = requests.get(
            self.issuer + "/.well-known/openid-configuration"
        )
        userinfo_url = issuer_oidc_config.json()["userinfo_endpoint"]
        resp = requests.get(
            userinfo_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        if resp.status_code == 200:
            return UserInfo(info=resp.json())
        raise TokenInvalid("Provided token not valid with relevant issuer.")

    def validate_token(self, token: str) -> UserInfo:
        """Try to validate the token against the give OIDC provider."""
        # TODO Handle validation exceptions
        parsed_token = AuthToken(
            **dict(zip(["bearer", "method", "provider", "token"], token.split("/")))
        )

        if parsed_token.method.value == AuthMethod.OIDC:
            # TODO Do we care about the provider ? Regardless of the provider,
            # I will submit the token to the issuer and it will be valid, or not.
            if parsed_token.provider.value == AuthProvider.EGI:
                return self._validate_oidc_token(parsed_token.token)

        raise TokenNotValidated("It was not possible to validate the provided token.")
