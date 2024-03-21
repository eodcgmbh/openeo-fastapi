import json

import fsspec
from fastapi.testclient import TestClient


def test_create_job(
    mocked_oidc_config, mocked_oidc_userinfo, job_post, core_api, app_settings
):
    """Test the /jobs POST endpoint as intended."""

    fake_job_json = json.dumps(job_post)

    test_app = TestClient(core_api.app)

    response = test_app.post(
        f"/{app_settings.OPENEO_VERSION}/jobs",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
        data=fake_job_json,
    )

    assert response.status_code == 201
    assert "access-control-expose-headers" in response.headers.keys()
