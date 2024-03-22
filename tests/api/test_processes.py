from fastapi.testclient import TestClient


def test_get_processes(core_api, app_settings):
    """Test the /processes endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/processes")

    assert response.status_code == 200
    assert "processes" in response.json().keys()
