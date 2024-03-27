import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, BaseModel, Extra, Field, validator


class JsonSchemaType(Enum):
    array = "array"
    boolean = "boolean"
    integer = "integer"
    null = "null"
    number = "number"
    object = "object"
    string = "string"


class Type1(Enum):
    Collection = "Collection"


class Type2(Enum):
    spatial = "spatial"
    temporal = "temporal"
    bands = "bands"
    other = "other"


class Type5(Enum):
    Catalog = "Catalog"


class Method(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


class Status(Enum):
    created = "created"
    queued = "queued"
    running = "running"
    canceled = "canceled"
    finished = "finished"
    error = "error"


class Level(Enum):
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


class GisDataType(Enum):
    raster = "raster"
    vector = "vector"
    table = "table"
    other = "other"


class RFC3339Datetime(BaseModel):
    """Class to consistently represent datetimes as strings compliant to RFC3339Datetime."""

    __root__: str = Field(
        description="", regex=r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"
    )

    @validator("__root__", pre=True)
    def ensure_non_fractional_and_timezone(cls, v):
        if isinstance(v, datetime.datetime):
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")
        return v


class JsonSchema(BaseModel):
    class Config:
        extra = Extra.allow

    type: Optional[Union[JsonSchemaType, list[JsonSchemaType]]] = Field(
        None,
        description="The allowed basic data type(s) for a value according to [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.1.1).\n\nIf this property is not present, all data types are allowed.",
    )
    subtype: Optional[str] = Field(
        None,
        description="The allowed sub data type for a value. See the chapter on [subtypes](#section/Processes/Defining-Processes) for more information.",
    )
    pattern: Optional[str] = Field(
        None,
        description="The regular expression a string value must match against. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.3.3).",
    )
    enum: Optional[list] = Field(
        None,
        description="An exclusive list of allowed values. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.1.2).",
    )
    minimum: Optional[float] = Field(
        None,
        description="The minimum value (inclusive) allowed for a numerical value. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.2.4).",
    )
    maximum: Optional[float] = Field(
        None,
        description="The maximum value (inclusive) allowed for a numerical value. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.2.2).",
    )
    minItems: Optional[float] = Field(
        None,
        ge=0.0,
        description="The minimum number of items required in an array. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.4.4).",
    )
    maxItems: Optional[float] = Field(
        None,
        ge=0.0,
        description="The maximum number of items required in an array. See [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.4.3).",
    )
    items: Optional[Union[list[dict], dict]] = Field(
        None,
        description="Specifies schemas for the items in an array according to [JSON Schema draft-07](https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.6.4.1).",
    )
    deprecated: Optional[bool] = None


class Endpoint(BaseModel):
    path: str = Field(
        ...,
        description="Path to the endpoint, relative to the URL of this endpoint. In general the paths MUST follow the paths specified in the openAPI specification as closely as possible. Therefore, paths MUST be prepended with a leading slash, but MUST NOT contain a trailing slash. Variables in the paths MUST be placed in curly braces and follow the parameter names in the openAPI specification, e.g. `{job_id}`.",
    )
    methods: list[Method] = Field(
        ...,
        description="Supported HTTP verbs in uppercase. It is OPTIONAL to list `OPTIONS` as method (see the [CORS section](#section/Cross-Origin-Resource-Sharing-(CORS))).",
    )


class Plan(BaseModel):
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
    value: float
    unit: str


class Usage(BaseModel):
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
    path: Optional[list[JsonSchema]] = Field(
        None,
        description="Describes where the log entry originates from.\n\nThe first element of the array is the process that has triggered the log entry, the second element is the parent of the process that has triggered the log entry, etc. This pattern is followed until the root of the process graph.",
    )
    usage: Optional[Usage]
    links: Optional[list[Link]]


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


class Error(BaseModel):
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


class Storage1(BaseModel):
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
