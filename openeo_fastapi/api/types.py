"""Pydantic Models and Enums describining different attribute types used by the models in openeo_fastapi.api.models."""
import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Union

from pydantic import AnyUrl, BaseModel, Extra, Field, validator


class STACConformanceClasses(Enum):
    """Available conformance classes with STAC."""
    CORE = "https://api.stacspec.org/v1.0.0/core"
    COLLECTIONS = "https://api.stacspec.org/v1.0.0/collections"


class DinensionEnum(Enum):
    """Dimension enum."""
    spatial = "spatial"
    temporal = "temporal"
    bands = "bands"
    other = "other"


class Type5(Enum):
    """Catalog enum."""
    Catalog = "Catalog"


class Method(Enum):
    """HTTP Methods enum."""
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


class Status(Enum):
    """Job Status enum."""
    created = "created"
    queued = "queued"
    running = "running"
    canceled = "canceled"
    finished = "finished"
    error = "error"


class Level(Enum):
    """Log level enum."""
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


class GisDataType(Enum):
    """Data type enum."""
    raster = "raster"
    vector = "vector"
    table = "table"
    other = "other"

class Role(Enum):
    """Role for collection provider."""
    producer = "producer"
    licensor = "licensor"
    processor = "processor"
    host = "host"


class RFC3339Datetime(BaseModel):
    """Model to consistently represent datetimes as strings compliant to RFC3339Datetime."""

    __root__: str = Field(
        description="", regex=r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"
    )

    @validator("__root__", pre=True)
    def ensure_non_fractional_and_timezone(cls, v):
        if isinstance(v, datetime.datetime):
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")
        return v


class Endpoint(BaseModel):
    """Model to capture the available endpoint and it's accepted models."""
    path: str = Field(
        ...,
        description="Path to the endpoint, relative to the URL of this endpoint. In general the paths MUST follow the paths specified in the openAPI specification as closely as possible. Therefore, paths MUST be prepended with a leading slash, but MUST NOT contain a trailing slash. Variables in the paths MUST be placed in curly braces and follow the parameter names in the openAPI specification, e.g. `{job_id}`.",
    )
    methods: list[Method] = Field(
        ...,
        description="Supported HTTP verbs in uppercase. It is OPTIONAL to list `OPTIONS` as method (see the [CORS section](#section/Cross-Origin-Resource-Sharing-(CORS))).",
    )


class Plan(BaseModel):
    """Model to capture the the plan the user has subscribe to."""
    name: str = Field(
        ...,
        description="Name of the plan. It MUST be accepted in a *case insensitive* manner throughout the API.",
        example="free",
    )
    description: str = Field(
        ...,
        description="A description that gives a rough overview over the plan.\n\n[CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation.",
        example="Free plan for testing.",
    )
    paid: bool = Field(
        ...,
        description="Indicates whether the plan is a paid plan (`true`) or a free plan (`false`).",
    )
    url: Optional[AnyUrl] = Field(
        None,
        description="URL to a web page with more details about the plan.",
        example="http://cool-cloud-corp.com/plans/free-plan",
    )


class Billing(BaseModel):
    """Model to capture the billing options that are available at the backend."""
    currency: str = Field(
        ...,
        description="The currency the back-end is billing in. The currency MUST be either a valid currency code as defined in ISO-4217 or a proprietary currency, e.g. tiles or back-end specific credits. If set to the default value `null`, budget and costs are not supported by the back-end and users can't be charged.",
        example="USD",
    )
    default_plan: Optional[str] = Field(
        None,
        description="Name of the default plan to use when the user doesn't specify a plan or has no default plan has been assigned for the user.",
        example="free",
    )
    plans: Optional[list[Plan]] = Field(
        None,
        description="Array of plans",
        example=[
            {
                "name": "free",
                "description": "Free plan. Calculates one tile per second and a maximum amount of 100 tiles per hour.",
                "url": "http://cool-cloud-corp.com/plans/free-plan",
                "paid": False,
            },
            {
                "name": "premium",
                "description": "Premium plan. Calculates unlimited tiles and each calculated tile costs 0.003 USD.",
                "url": "http://cool-cloud-corp.com/plans/premium-plan",
                "paid": True,
            },
        ],
    )


class File(BaseModel):
    """Model to capture the stat information of a file stored at the backend."""
    path: str = Field(
        ...,
        description="Path of the file, relative to the root directory of the user's server-side workspace.\nMUST NOT start with a slash `/` and MUST NOT be url-encoded.\n\nThe Windows-style path name component separator `\\` is not supported,\nalways use `/` instead.\n\nNote: The pattern only specifies a minimal subset of invalid characters.\nThe back-ends MAY enforce additional restrictions depending on their OS/environment.",
        example="folder/file.txt",
    )
    size: Optional[int] = Field(None, description="File size in bytes.", example=1024)
    modified: Optional[RFC3339Datetime] = Field(
        None,
        description="Date and time the file has lastly been modified, formatted as a [RFC 3339](https://www.rfc-editor.org/rfc/RFC3339Datetime.html) date-time.",
        example="2018-01-03T10:55:29Z",
    )


class UsageMetric(BaseModel):
    """Model to capture the value and unit of a given metric."""
    value: float
    unit: str


class Usage(BaseModel):
    """Model to capture the usage of a job."""
    class Config:
        extra = Extra.allow

    cpu: Optional[UsageMetric] = Field(
        None,
        description="Specifies the CPU usage, usually in a unit such as `cpu-seconds`.",
    )
    memory: Optional[UsageMetric] = Field(
        None,
        description="Specifies the memory usage, usually in a unit such as `mb-seconds` or `gb-hours`.",
    )
    duration: Optional[UsageMetric] = Field(
        None,
        description="Specifies the wall time, usually in a unit such as `seconds`, `minutes` or `hours`.",
    )
    network: Optional[UsageMetric] = Field(
        None,
        description="Specifies the network transfer usage (incoming and outgoing), usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )
    disk: Optional[UsageMetric] = Field(
        None,
        description="Specifies the amount of input (read) and output (write) operations on the storage such as disks, usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )
    storage: Optional[UsageMetric] = Field(
        None,
        description="Specifies the usage of storage space, usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )


class Link(BaseModel):
    """Model to describe the information for a provided URL."""
    rel: str = Field(
        ...,
        description="Relationship between the current document and the linked document. SHOULD be a [registered link relation type](https://www.iana.org/assignments/link-relations/link-relations.xml) whenever feasible.",
        example="related",
    )
    href: Union[AnyUrl, Path] = Field(
        ...,
        description="The value MUST be a valid URL.",
        example="https://example.openeo.org",
    )
    type: Optional[str] = Field(
        None,
        description="The value MUST be a string that hints at the format used to represent data at the provided URI, preferably a media (MIME) type.",
        example="text/html",
    )
    title: Optional[str] = Field(
        None, description="Used as a human-readable label for a link.", example="openEO"
    )


class LogEntry(BaseModel):
    """Model to describe the information for a given log line in job logs."""
    id: str = Field(
        ...,
        description="An unique identifier for the log message, could simply be an incrementing number.",
        example="1",
    )
    code: Optional[str]
    level: Level = Field(
        ...,
        description="The severity level of the log entry.\n\nThe order of the levels is as follows (from high to low severity): `error`, `warning`, `info`, `debug`.\n\nThe level `error` usually stops processing the data.",
        example="error",
    )
    message: str = Field(
        ...,
        description="A message explaining the log entry.",
        example="Can't load the UDF file from the URL `https://example.com/invalid/file.txt`. Server responded with error 404.",
    )
    time: Optional[RFC3339Datetime] = Field(
        None,
        description="The date and time the event happened, in UTC. Formatted as a [RFC 3339](https://www.rfc-editor.org/rfc/RFC3339Datetime.html) date-time.",
        title="Date and Time",
    )
    data: Optional[Any] = Field(
        None,
        description="Data of any type. It is the back-ends task to decide how to best\npresent passed data to a user.\n\nFor example, a raster-cube passed to the `debug` SHOULD return the\nmetadata similar to the collection metadata, including `cube:dimensions`.",
    )
    path: Optional[list[str]] = Field(
        None,
        description="Describes where the log entry originates from.\n\nThe first element of the array is the process that has triggered the log entry, the second element is the parent of the process that has triggered the log entry, etc. This pattern is followed until the root of the process graph.",
    )
    usage: Optional[Usage]
    links: Optional[list[Link]]


class Process(BaseModel):
    """Model to describe a process that is exposed by the api."""
    id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[list[str]] = None
    parameters: Optional[list[dict[str, Union[list[Any], Any]]]] = None
    returns: Optional[dict[str, Union[list[Any], Any]]] = None
    deprecated: Optional[bool] = None
    experimental: Optional[bool] = None
    exceptions: Optional[dict[str, Union[list[Any], Any]]] = None
    examples: Optional[list[dict[str, Union[list[Any], Any]]]] = Field(
        None, description="Examples, may be used for unit tests."
    )
    links: Optional[list[Link]] = Field(
        None,
        description="Links related to this process, e.g. additional external documentation.\nIt is RECOMMENDED to provide links with the following `rel` (relation) types:\n1. `latest-version`: If a process has been marked as deprecated, a link SHOULD point to the preferred version of the process. The relation types `predecessor-version` (link to older version) and `successor-version` (link to newer version) can also be used to show the relation between versions.\n2. `example`: Links to examples of other processes that use this process.\n3. `cite-as`: For all DOIs associated with the process, the respective DOI links SHOULD be added.\nFor additional relation types see also the lists of [common relation types in openEO](#section/API-Principles/Web-Linking).",
    )
    process_graph: Optional[dict[str, Union[list[Any], Any]]] = None


class Error(BaseModel):
    """Model to describe the information of a captured exception by the api."""
    id: Optional[str] = Field(
        None,
        description="A back-end MAY add a unique identifier to the error response to be able to log and track errors with further non-disclosable details. A client could communicate this id to a back-end provider to get further information.",
        example="550e8400-e29b-11d4-a716-446655440000",
    )
    code: str
    message: str = Field(
        ...,
        description="A message explaining what the client may need to change or what difficulties the server is facing.",
        example="Parameter 'sample' is missing.",
    )
    links: Optional[list[Link]] = None


class FileFormat(BaseModel):
    """Model to describe a file format supported by the processing backend."""
    title: str
    description: Optional[str] = None
    gis_data_types: list[GisDataType] = Field(
        ...,
        description="Specifies the supported GIS spatial data types for this format.\nIt is RECOMMENDED to specify at least one of the data types, which will likely become a requirement in a future API version.",
    )
    deprecated: Optional[bool] = None
    experimental: Optional[bool] = None
    parameters: dict[str, Any] = Field(
        ...,
        description="Specifies the supported parameters for this file format.",
        title="File Format Parameters",
    )
    links: Optional[list[Link]] = Field(
        None,
        description="Links related to this file format, e.g. external documentation.\n\nFor relation types see the lists of\n[common relation types in openEO](#section/API-Principles/Web-Linking).",
    )


class Storage(BaseModel):
    """Model to describe the storage resources available to a given user."""
    free: int = Field(
        ...,
        description="Free storage space in bytes, which is still available to the user. Effectively, this is the disk quota minus the used space by the user, e.g. user-uploaded files and job results.",
        example=536870912,
    )
    quota: int = Field(
        ...,
        description="Maximum storage space (disk quota) in bytes available to the user.",
        example=1073741824,
    )


class Version(BaseModel):
    """Model to describe the version of an api that is available."""
    url: AnyUrl = Field(
        ...,
        description="*Absolute* URLs to the service.",
        example="https://example.com/api/v1.0",
    )
    production: Optional[bool] = None
    api_version: str = Field(
        ...,
        description="Version number of the openEO specification this back-end implements.",
    )
    
class StacProvider(BaseModel):
    """Model to describe the provider of a given stac resource."""
    name: str = Field(
        ...,
        description="The name of the organization or the individual.",
        example="Cool EO Cloud Corp",
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Multi-line description to add further provider information such as processing details for "
            "processors and producers, hosting details for hosts or basic contact information."
            "CommonMark 0.29 syntax MAY be used for rich text representation."
        ),
        example="No further processing applied.",
    )
    roles: Optional[list[Role]] = Field(
        None,
        description=(
            "Roles of the provider.\n\nThe provider's role(s) can be one or more of the following "
            "elements:\n* licensor: The organization that is licensing the dataset under the license"
            "specified in the collection's license field.\n* producer: The producer of the data is the"
            "provider that initially captured and processed the source data, e.g. ESA for Sentinel-2 data."
            "* processor: A processor is any provider who processed data to a derived product.\n* host: The"
            "host is the actual provider offering the data on their storage. There SHOULD be no more than"
            "one host, specified as last element of the list."
        ),
        example=["producer", "licensor", "host"],
    )
    url: Optional[AnyUrl] = Field(
        None,
        description=(
            "Homepage on which the provider describes the dataset and publishes contact information."
        ),
        example="http://cool-eo-cloud-corp.com",
    )


class Dimension(BaseModel):
    """Model to describe the dimension of some data."""
    type: DinensionEnum = Field(..., description="Type of the dimension.")
    description: Optional[str] = None


class Spatial(BaseModel):
    """Model to describe the spatial extent of a collection."""
    bbox: Optional[list[list[float]]] = Field(
        None,
        description=(
            "One or more bounding boxes that describe the spatial extent\nof the dataset."
            "The first bounding box describes the overall spatial extent\nof the data. All "
            "subsequent bounding boxes describe more\nprecise bounding boxes, e.g. to identify "
            "clusters of data.\nClients only interested in the overall spatial extent will "
            "only need to access the first item in each array."
        ),
        min_items=1,
    )


class Temporal(BaseModel):
    """Model to describe the temporal range of a collection."""
    interval: Optional[list[list[Any]]] = Field(
        None,
        description=(
            "One or more time intervals that describe the temporal extent of the dataset."
            "The first time interval describes the overall temporal extent of the data. "
            "All subsequent time intervals describe more precise time intervals, e.g. to "
            "identify clusters of data. Clients only interested in the overall extent will"
            "only need to access the first item in each array."
        ),
        min_items=1,
    )


class Extent(BaseModel):
    """Model to describe the complete spatiotemporal extent of a collection."""
    spatial: Spatial = Field(
        ...,
        description="The *potential* spatial extents of the features in the collection.",
        title="Collection Spatial Extent",
    )
    temporal: Temporal = Field(
        ...,
        description="The *potential* temporal extents of the features in the collection.",
        title="Collection Temporal Extent",
    )
