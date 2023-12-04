import abc
import json

from attrs import define
from fastapi import Response


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    @abc.abstractmethod
    def get_capabilities(self):
        """ """
        return Response(status_code=200, content=json.dumps({"version": "1"}))
