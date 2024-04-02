import json

from fastapi.testclient import TestClient

from tests.utils import patch_request, post_request, put_request


def test_get_processes(core_api, app_settings):
    """Test the /processes endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/processes")

    assert response.status_code == 200
    assert "processes" in response.json().keys()


def test_list_user_process_graphs(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings, process_graph
):
    """Test the /process_graphs endpoint as intended."""

    test_app = TestClient(core_api.app)

    resp = put_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        process_graph,
    )

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/process_graphs",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    _json = response.json()

    assert response.status_code == 200
    assert len(_json["processes"]) == 1
    assert _json["processes"][0]["id"] == process_graph["id"]


def test_get_user_process_graph(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings, process_graph
):
    """Test the /process_graphs endpoint as intended."""

    test_app = TestClient(core_api.app)

    put_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        process_graph,
    )

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == process_graph["id"]


def test_put_user_process_graph(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings, process_graph
):
    """Test the /process_graphs endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = put_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        process_graph,
    )

    assert response.status_code == 201
    
    # Try to create twice
    response = put_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        process_graph,
    )

    assert response.status_code == 500

def test_delete_user_process_graph(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings, process_graph
):
    """Test the /process_graphs endpoint as intended."""

    test_app = TestClient(core_api.app)

    test_app = TestClient(core_api.app)

    response = put_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        process_graph,
    )

    assert response.status_code == 201

    response = test_app.delete(
        f"/{app_settings.OPENEO_VERSION}/process_graphs/{process_graph['id']}",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 204

    response = test_app.delete(
        f"/{app_settings.OPENEO_VERSION}/process_graphs/doesntexist",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 404


def test_validate_user_process_graph(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings, process_graph
):
    """Test the /process_graphs endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = post_request(
        test_app,
        f"/{app_settings.OPENEO_VERSION}/validation",
        process_graph,
    )

    assert response.status_code == 201
