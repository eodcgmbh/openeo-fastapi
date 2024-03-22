import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Union

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
