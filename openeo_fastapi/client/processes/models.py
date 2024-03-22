import datetime
import uuid
from typing import Any, Optional, Union

from pydantic import BaseModel, Extra, Field

from openeo_fastapi.client.models import JsonSchema, Link
from openeo_fastapi.client.psql.models import ProcessGraphORM


class ProcessGraph(BaseModel):
    process_graph_id: str
    process_graph: dict
    user_id: uuid.UUID
    created: datetime.datetime

    @classmethod
    def get_orm(cls):
        return ProcessGraphORM

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = Extra.ignore


class Process(BaseModel):
    id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[list[str]] = None
    parameters: Optional[Union[JsonSchema, list[JsonSchema]]] = None
    returns: Optional[Union[JsonSchema, list[JsonSchema]]] = None
    deprecated: Optional[bool] = None
    experimental: Optional[bool] = None
    exceptions: Optional[Union[JsonSchema, list[JsonSchema]]] = None
    examples: Optional[Union[JsonSchema, list[JsonSchema]]] = Field(
        None, description="Examples, may be used for unit tests."
    )
    links: Optional[list[Link]] = Field(
        None,
        description="Links related to this process, e.g. additional external documentation.\nIt is RECOMMENDED to provide links with the following `rel` (relation) types:\n1. `latest-version`: If a process has been marked as deprecated, a link SHOULD point to the preferred version of the process. The relation types `predecessor-version` (link to older version) and `successor-version` (link to newer version) can also be used to show the relation between versions.\n2. `example`: Links to examples of other processes that use this process.\n3. `cite-as`: For all DOIs associated with the process, the respective DOI links SHOULD be added.\nFor additional relation types see also the lists of [common relation types in openEO](#section/API-Principles/Web-Linking).",
    )
    process_graph: Optional[JsonSchema] = None


class ProcessesGetResponse(BaseModel):
    processes: list[Process]
    links: list[Link]


class ProcessGraphWithMetadata(Process):
    process_graph_id: Any = Field(default=None, alias="id")
    summary: Optional[Any] = None
    description: Optional[Any] = None
    parameters: Optional[Any] = None
    returns: Optional[Any] = None
    process_graph: Any = None

    class Config:
        allow_population_by_field_name = True
