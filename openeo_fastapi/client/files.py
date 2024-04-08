"""Class and model to define the framework and partial application logic for interacting with Files.

Classes:
    - FilesRegister: Framework for defining and extending the logic for working with Files.
"""
from fastapi import Depends, HTTPException
from typing import Optional

from openeo_fastapi.api.types import Endpoint, Error
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.register import EndpointRegister

FILE_ENDPOINTS = [
    Endpoint(
        path="/files",
        methods=["GET"],
    ),
    Endpoint(
        path="/files/{path}",
        methods=["GET"],
    ),
    Endpoint(
        path="/files/{path}",
        methods=["PUT"],
    ),
    Endpoint(
        path="/files/{path}",
        methods=["DELETE"],
    ),
]


class FilesRegister(EndpointRegister):
    def __init__(self, settings, links) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.settings = settings
        self.links = links

    def _initialize_endpoints(self) -> list[Endpoint]:
        return FILE_ENDPOINTS

    def list_files(
        self, limit: Optional[int] = 10, user: User = Depends(Authenticator.validate)
    ):
        """List the  files in the user workspace.

        Args:
            limit (int): The limit to apply to the length of the list.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def download_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """Download the file from the user's workspace.

        Args:
            path (str): The path leading to the file.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def upload_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """Upload the file from the user's workspace.

        Args:
            path (str): The path leading to the file.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def delete_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """Delete the file from the user's workspace.

        Args:
            path (str): The path leading to the file.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )
