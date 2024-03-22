import json
import uuid

from fastapi.testclient import TestClient


def post_request(app: TestClient, path: str, data: dict):
    """Code to post a job to the provided client."""
    payload = json.dumps(data)

    response = app.post(
        path,
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
        data=payload,
    )

    return response


def patch_request(app: TestClient, path: str, data: dict):
    """Code to post a job to the provided client."""
    payload = json.dumps(data)

    response = app.patch(
        path,
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
        data=payload,
    )

    return response


def test_list_jobs(
    mocked_oidc_config, mocked_oidc_userinfo, job_post, core_api, app_settings
):
    """Test the /jobs GET endpoint as intended."""

    test_app = TestClient(core_api.app)

    for x in range(0, 3):
        job_post["process"]["id"] = uuid.uuid4().hex[:16].upper()
        post_request(
            test_app, f"/{app_settings.OPENEO_VERSION}/jobs", job_post
        ).status_code

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/jobs",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200
    # assert response.content == "content"
    assert len(response.json()["jobs"]) == 3


def test_create_job(
    mocked_oidc_config, mocked_oidc_userinfo, job_post, core_api, app_settings
):
    """Test the /jobs POST endpoint as intended."""

    test_app = TestClient(core_api.app)
    job_post["process"]["id"] = uuid.uuid4().hex[:16].upper()

    response = post_request(test_app, f"/{app_settings.OPENEO_VERSION}/jobs", job_post)

    assert response.status_code == 201
    assert "access-control-expose-headers" in response.headers.keys()
    assert "openeo-identifier" in response.headers.keys()


def test_update_job(
    mocked_oidc_config, mocked_oidc_userinfo, job_post, core_api, app_settings
):
    """Test the /jobs/{job_id} POST endpoint as intended."""

    test_app = TestClient(core_api.app)
    job_post["process"]["id"] = uuid.uuid4().hex[:16].upper()

    response = post_request(test_app, f"/{app_settings.OPENEO_VERSION}/jobs", job_post)

    job_id = response.headers["openeo-identifier"]

    new_pg_id = uuid.uuid4().hex[:16].upper()
    updated_pg = {"process": {"id": new_pg_id, "process_graph": {"func": "new-arg"}}}

    response = patch_request(
        test_app, f"/{app_settings.OPENEO_VERSION}/jobs/{job_id}", updated_pg
    )

    assert response.status_code == 204

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/jobs/{job_id}",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.json()["process"]["id"] == new_pg_id


def test_get_job(
    mocked_oidc_config, mocked_oidc_userinfo, job_post, core_api, app_settings
):
    """Test the /jobs/{job_id} GET endpoint as intended."""

    test_app = TestClient(core_api.app)
    job_post["process"]["id"] = uuid.uuid4().hex[:16].upper()

    response = post_request(test_app, f"/{app_settings.OPENEO_VERSION}/jobs", job_post)

    job_id = response.headers["openeo-identifier"]

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/jobs/{job_id}",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200
