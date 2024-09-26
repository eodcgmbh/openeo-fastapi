import uuid

from fastapi.testclient import TestClient


def test_not_implemented(
    mocked_oidc_config,
    mocked_oidc_userinfo,
    mocked_get_oidc_jwks,
    mocked_validate_token,
    core_api,
    app_settings,
):
    """
    Test the following endpoints are initialised correctly, but return an error.

    /files GET
    /files/{path} GET
    /files/{path} PUT
    /files/{path} DELETE
    """

    def assert_not(response):
        assert response.status_code == 501
        assert response.json()["code"] == "FeatureUnsupported"

    test_app = TestClient(core_api.app)

    gets = [
        f"{app_settings.OPENEO_PREFIX}/files",
        f"{app_settings.OPENEO_PREFIX}/files/somefile.txt",
    ]

    for get in gets:
        assert_not(
            test_app.get(
                get,
                headers={"Authorization": "Bearer /oidc/egi/not-real"},
            )
        )

    puts = [f"{app_settings.OPENEO_PREFIX}/files/somefile.txt"]

    for post in puts:
        assert_not(
            test_app.put(
                post,
                headers={"Authorization": "Bearer /oidc/egi/not-real"},
            )
        )

    deletes = [f"{app_settings.OPENEO_PREFIX}/files/somefile.txt"]

    for delete in deletes:
        assert_not(
            test_app.delete(
                delete,
                headers={"Authorization": "Bearer /oidc/egi/not-real"},
            )
        )
