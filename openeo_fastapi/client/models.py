import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Union

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


class ConformanceGetResponse(BaseModel):
    conformsTo: list[AnyUrl]


class Version(BaseModel):
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


class WellKnownOpeneoGetResponse(BaseModel):
    versions: list[Version]


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


class Capabilities(BaseModel):
    api_version: str = Field(
        ...,
        description="Version number of the openEO specification this back-end implements.",
    )
    backend_version: str = Field(
        ...,
        description="Version number of the back-end implementation.\nEvery change on back-end side MUST cause a change of the version number.",
        example="1.1.2",
    )
    stac_version: str
    type: Optional[Type5] = Field(
        None,
        description="For STAC versions >= 1.0.0-rc.1 this field is required.",
        example="Catalog",
    )
    id: str = Field(
        ...,
        description="Identifier for the service.\nThis field originates from STAC and is used as unique identifier for the STAC catalog available at `/collections`.",
        example="cool-eo-cloud",
    )
    title: str = Field(
        ..., description="The name of the service.", example="Cool EO Cloud"
    )
    description: str = Field(
        ...,
        description="A description of the service, which allows the service provider to introduce the user to its service.\n[CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation.",
        example="This service is provided to you by [Cool EO Cloud Corp.](http://cool-eo-cloud-corp.com). It implements the full openEO API and allows to process a range of 999 EO data sets, including \n\n* Sentinel 1/2/3 and 5\n* Landsat 7/8\n\nA free plan is available to test the service. For further information please contact our customer service at [support@cool-eo-cloud-corp.com](mailto:support@cool-eo-cloud-corp.com).",
    )
    production: Optional[bool] = None
    endpoints: list[Endpoint] = Field(
        ...,
        description="Lists all supported endpoints. Supported are all endpoints, which are implemented, return a 2XX or 3XX HTTP status code and are fully compatible to the API specification. An entry for this endpoint (path `/` with method `GET`) SHOULD NOT be listed.",
        example=[
            {"path": "/collections", "methods": ["GET"]},
            {"path": "/collections/{collection_id}", "methods": ["GET"]},
            {"path": "/processes", "methods": ["GET"]},
            {"path": "/jobs", "methods": ["GET", "POST"]},
            {"path": "/jobs/{job_id}", "methods": ["GET", "DELETE", "PATCH"]},
        ],
    )
    billing: Optional[Billing] = Field(
        None,
        description="Billing related data, e.g. the currency used or available plans to process jobs.\nThis property MUST be specified if the back-end uses any billing related API functionalities, e.g. budgeting or estimates.\nThe absence of this property doesn't mean the back-end is necessarily free to use for all. Providers may choose to bill users outside of the API, e.g. with a monthly fee that is not depending on individual API interactions.",
        title="Billing",
    )
    links: list[Link] = Field(
        ...,
        description="Links related to this service, e.g. the homepage of\nthe service provider or the terms of service.\n\nIt is highly RECOMMENDED to provide links with the\nfollowing `rel` (relation) types:\n\n1. `version-history`: A link back to the Well-Known URL\n(see `/.well-known/openeo`) to allow clients to work on\nthe most recent version.\n\n2. `terms-of-service`: A link to the terms of service. If\na back-end provides a link to the terms of service, the\nclients MUST provide a way to read the terms of service\nand only connect to the back-end after the user agreed to\nthem. The user interface MUST be designed in a way that\nthe terms of service are not agreed to by default, i.e.\nthe user MUST explicitly agree to them.\n\n3. `privacy-policy`: A link to the privacy policy (GDPR).\nIf a back-end provides a link to a privacy policy, the\nclients MUST provide a way to read the privacy policy and\nonly connect to the back-end after the user agreed to\nthem. The user interface MUST be designed in a way that\nthe privacy policy is not agreed to by default, i.e. the\nuser MUST explicitly agree to them.\n\n4. `service-desc` or `service-doc`: A link to the API definition.\nUse `service-desc` for machine-readable API definition and \n`service-doc` for human-readable API definition.\nRequired if full OGC API compatibility is desired.\n\n5. `conformance`: A link to the Conformance declaration\n(see `/conformance`). \nRequired if full OGC API compatibility is desired.\n\n6. `data`: A link to the collections (see `/collections`).\nRequired if full OGC API compatibility is desired.\n\nFor additional relation types see also the lists of\n[common relation types in openEO](#section/API-Principles/Web-Linking).",
        example=[
            {
                "href": "http://www.cool-cloud-corp.com",
                "rel": "about",
                "type": "text/html",
                "title": "Homepage of the service provider",
            },
            {
                "href": "https://www.cool-cloud-corp.com/tos",
                "rel": "terms-of-service",
                "type": "text/html",
                "title": "Terms of Service",
            },
            {
                "href": "https://www.cool-cloud-corp.com/privacy",
                "rel": "privacy-policy",
                "type": "text/html",
                "title": "Privacy Policy",
            },
            {
                "href": "http://www.cool-cloud-corp.com/.well-known/openeo",
                "rel": "version-history",
                "type": "application/json",
                "title": "List of supported openEO versions",
            },
            {
                "href": "http://www.cool-cloud-corp.com/api/v1.0/conformance",
                "rel": "conformance",
                "type": "application/json",
                "title": "OGC Conformance Classes",
            },
            {
                "href": "http://www.cool-cloud-corp.com/api/v1.0/collections",
                "rel": "data",
                "type": "application/json",
                "title": "List of Datasets",
            },
        ],
    )


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
