from unittest.mock import patch

import pytest
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from openeo_fastapi.client import auth

BASIC_TOKEN_EXAMPLE = "Bearer basic/openeo/rubbish.not.a.token"
OIDC_TOKEN_EXAMPLE = "Bearer oidc/issuer/rubbish.not.a.token"

INVALID_TOKEN_EXAMPLE_1 = "bearer /basic/openeo/rubbish.not.a.token"
INVALID_TOKEN_EXAMPLE_2 = "Bearer /basicopeneorubbish.not.a.token"
INVALID_TOKEN_EXAMPLE_3 = "Bearer //openeo/rubbish.not.a.token"
INVALID_TOKEN_EXAMPLE_4 = "Bearer /basic//rubbish.not.a.token"
INVALID_TOKEN_EXAMPLE_5 = "Bearer /basic/openeo/"
INVALID_TOKEN_EXAMPLE_6 = "Bearer /basic/openeo/rubbish.not.a.token"


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
        assert token.method.value == method
        assert token.provider == provider

    basic_token = auth.AuthToken.from_token(BASIC_TOKEN_EXAMPLE)
    token_checks(basic_token, "basic", "openeo")

    oidc_token = auth.AuthToken.from_token(OIDC_TOKEN_EXAMPLE)
    token_checks(oidc_token, "oidc", "issuer")

    # Check cases of invalid format raise a validation error.
    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_1)

    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_2)

    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_3)

    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_4)

    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_5)

    with pytest.raises(ValidationError):
        auth.AuthToken.from_token(INVALID_TOKEN_EXAMPLE_6)


def test_issuer_handler_init():
    test_issuer = auth.IssuerHandler(
        issuer_uri="http://issuer.mycloud/",
        policies=["groups,/dev-staff", " groups,/admin-staff"],
    )

    # Check trailing slash removal
    assert not test_issuer.issuer_uri.endswith("/")
    assert len(test_issuer.policies) == 2


def test_issuer_handler__validate_oidc_token(
    mocked_oidc_config,
    mocked_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    mocked_issuer,
):
    info = mocked_issuer._authenticate_oidc_user(token=OIDC_TOKEN_EXAMPLE)
    assert info


def test_issuer_handler__validate_oidc_token_bad_config(
    mocked_bad_oidc_config,
    mocked_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    mocked_issuer,
):
    with pytest.raises(HTTPException):
        mocked_issuer._authenticate_oidc_user(token=OIDC_TOKEN_EXAMPLE)


def test_issuer_handler__validate_oidc_token_bad_userinfo(
    mocked_oidc_config,
    mocked_bad_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    mocked_issuer,
):
    with pytest.raises(HTTPException):
        mocked_issuer._authenticate_oidc_user(token=OIDC_TOKEN_EXAMPLE)


def test_issuer_handler_validate_oidc_token(
    mocked_oidc_config,
    mocked_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    mocked_issuer,
):
    info = mocked_issuer.validate_token(token=OIDC_TOKEN_EXAMPLE)
    assert info


def test_issuer_handler_validate_basic_token(
    mocked_oidc_config,
    mocked_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    mocked_issuer,
):
    with pytest.raises(HTTPException):
        mocked_issuer.validate_token(token=BASIC_TOKEN_EXAMPLE)


def test_issuer_handler_validate_broken_token(
    mocked_oidc_config, mocked_oidc_userinfo, mocked_issuer
):
    with pytest.raises(ValidationError):
        mocked_issuer.validate_token(token=INVALID_TOKEN_EXAMPLE_1)


def test_validate_token(mocked_oidc_token, mocked_oidc_jwks):
    test_issuer = auth.IssuerHandler(
        issuer_uri="http://issuer.mycloud/",
    )

    # Mocks in situ for one time use
    with patch("jose.jwt.get_unverified_header") as mock_get_unverified_header:
        mock_get_unverified_header.return_value = {"kid": "1b94c"}

        # Mock the jwt.decode to return a payload
        with patch("jose.jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {
                "sub": "1234567890",
                "name": "John Doe",
                "email": "john.doe@example.com",
            }

            # Call the function under test
            payload = test_issuer._validate_token(mocked_oidc_token, mocked_oidc_jwks)

            # Assertions
            assert payload["sub"] == "1234567890"
            assert payload["name"] == "John Doe"
            assert payload["email"] == "john.doe@example.com"
