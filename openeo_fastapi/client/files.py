from typing import Optional

from fastapi import Depends, HTTPException

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
        """_summary_

        Args:
            limit (int): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def download_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            path (str): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def upload_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            path (str): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def delete_file(self, path: str, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            path (str): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )
