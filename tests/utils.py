import json

from fastapi.testclient import TestClient


def post_request(app: TestClient, path: str, data: dict):
    """
    Code to post a job to the provided client.
    """
    payload = json.dumps(data)

    response = app.post(
        path,
        headers={"Authorization": "Bearer oidc/egi/not-real"},
        data=payload,
    )

    return response


def patch_request(app: TestClient, path: str, data: dict):
    """
    Code to post a job to the provided client.
    """
    payload = json.dumps(data)

    response = app.patch(
        path,
        headers={"Authorization": "Bearer oidc/egi/not-real"},
        data=payload,
    )

    return response


def put_request(app: TestClient, path: str, data: dict):
    """
    Code to post a job to the provided client.
    """
    payload = json.dumps(data)

    response = app.put(
        path,
        headers={"Authorization": "Bearer oidc/egi/not-real"},
        data=payload,
    )

    return response
