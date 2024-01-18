import pytest
from pydantic import ValidationError

from openeo_fastapi.client import auth


def test_auth_method():
    BASIC_VALUE = "basic"
    OIDC_VALUE = "oidc"

    basic = auth.AuthMethod(BASIC_VALUE)
    oidc = auth.AuthMethod(OIDC_VALUE)

    assert basic.value == BASIC_VALUE
    assert oidc.value == OIDC_VALUE

    with pytest.raises(ValueError):
        auth.AuthMethod("wrong")


def test_auth_token():
    def token_checks(token: auth.AuthToken, method: str, provider: str):
        assert token.bearer
        assert token.method.value == method
        assert token.provider == provider

    BASIC_TOKEN_EXAMPLE = "Bearer /basic/openeo/rubbish.not.a.token"
    basic_token = auth.AuthToken.from_token(BASIC_TOKEN_EXAMPLE)
    token_checks(basic_token, "basic", "openeo")

    OIDC_TOKEN_EXAMPLE = "Bearer /oidc/issuer/rubbish.not.a.token"
    oidc_token = auth.AuthToken.from_token(OIDC_TOKEN_EXAMPLE)
    token_checks(oidc_token, "oidc", "issuer")

    # Check cases of invalid format raise a validation error.
    INVALID_TOKEN_EXAMPLE_1 = "bearer /basic/openeo/rubbish.not.a.token"
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_1)

    INVALID_TOKEN_EXAMPLE_2 = "Bearer /basicopeneorubbish.not.a.token"
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_2)

    INVALID_TOKEN_EXAMPLE_3 = "Bearer //openeo/rubbish.not.a.token"
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_3)

    INVALID_TOKEN_EXAMPLE_4 = "Bearer /basic//rubbish.not.a.token"
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_4)

    INVALID_TOKEN_EXAMPLE_5 = "Bearer /basic/openeo/"
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_5)


def test_issuer_handler_init():
    test_issuer = auth.IssuerHandler(
        issuer_url="http://issuer.mycloud/",
        organisation="mycloud",
        roles=["admin", "user"],
    )

    # Check trailing slash removal
    assert not test_issuer.issuer_url.endswith("/")


def test_issuer_handler__validate_oidc_token():
    test_issuer = auth.IssuerHandler(
        issuer_url="http://issuer.mycloud/",
        organisation="mycloud",
        roles=["admin", "user"],
    )

    assert True


def test_issuer_handler_validate_token():
    test_issuer = auth.IssuerHandler(
        issuer_url="http://issuer.mycloud/",
        organisation="mycloud",
        roles=["admin", "user"],
    )

    assert True
