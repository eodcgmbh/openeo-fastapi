import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict, Union

from pydantic import AnyUrl, BaseModel, Extra, Field, validator

from openeo_fastapi.api.types import (
    Billing,
    Endpoint,
    Error,
    File,
    FileFormat,
    Link,
    Process,
    RFC3339Datetime,
    Status,
    Storage1,
    Type1,
    Type2,
    Type5,
    Usage,
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


#############
# Collections
#############
class Role(Enum):
    producer = "producer"
    licensor = "licensor"
    processor = "processor"
    host = "host"


class StacProvider(BaseModel):
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


class StacProviders(BaseModel):
    __root__: list[StacProvider] = Field(
        ...,
        description=(
            "A list of providers, which MAY include all organizations capturing or processing "
            "the data or the hosting provider. Providers SHOULD be listed in chronological order"
            "with the most recent provider being the last element of the list."
        ),
    )


class Dimension(BaseModel):
    type: Type2 = Field(..., description="Type of the dimension.")
    description: Optional[str] = None


class Spatial(BaseModel):
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


class CollectionSummaryStats(BaseModel):
    min: Union[str, float] = Field(alias="minimum")
    max: Union[str, float] = Field(alias="maximum")


class Collection(BaseModel):
    stac_version: str
    stac_extensions: Optional[list[Union[AnyUrl, str]]] = None
    type: Optional[Type1] = Field(
        None, description="For STAC versions >= 1.0.0-rc.1 this field is required."
    )
    id: str
    title: Optional[str] = Field(
        None, description="A short descriptive one-line title for the collection."
    )
    description: str = Field(
        ...,
        description=(
            "Detailed multi-line description to explain the collection.\n\n"
            "[CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation."
        ),
    )
    keywords: Optional[list[str]] = Field(
        None, description="List of keywords describing the collection."
    )
    version: Optional[str] = Field(
        None,
        description=(
            "Version of the collection.\n\nThis property REQUIRES to add `version` (STAC < 1.0.0-rc.1)"
            "or\n`https://stac-extensions.github.io/version/v1.0.0/schema.json` (STAC >= 1.0.0-rc.1)\n"
            "to the list of `stac_extensions`."
        ),
    )
    deprecated: Optional[bool] = Field(
        False,
        description=(
            "Specifies that the collection is deprecated with the potential to\nbe removed. "
            "It should be transitioned out of usage as soon as\npossible and users should refrain from "
            "using it in new projects.\n\nA link with relation type `latest-version` SHOULD be added to "
            "the\nlinks and MUST refer to the collection that can be used instead.\n\nThis property "
            "REQUIRES to add `version` (STAC < 1.0.0-rc.1) or\n"
            "`https://stac-extensions.github.io/version/v1.0.0/schema.json` (STAC >= 1.0.0-rc.1)\n"
            "to the list of `stac_extensions`."
        ),
    )
    license: str
    providers: Optional[StacProviders] = None
    extent: Extent = Field(
        ...,
        description=(
            "The extent of the data in the collection. Additional members MAY\nbe added to "
            "represent other extents, for example, thermal or\npressure ranges.\n\nThe first "
            "item in the array always describes the overall extent of\nthe data. All subsequent "
            "items describe more preciseextents,\ne.g. to identify clusters of data.\nClients only "
            "interested in the overall extent will only need to\naccess the first item in each array."
        ),
        title="Collection Extent",
    )
    links: list[Link] = Field(
        ...,
        description=(
            "Links related to this collection. Could reference to licensing information, other meta data "
            "formats with additional information or a preview image.\nIt is RECOMMENDED to provide links "
            "with the following `rel` (relation) types:\n1. `root` and `parent`: URL to the data discovery "
            "endpoint at `/collections`.\n2. `license`: A link to the license(s) SHOULD be specified if the "
            "`license` field is set to `proprietary` or `various`.\n3. `example`: Links to examples of "
            "processes that use this collection.\n4. `latest-version`: If a collection has been marked as "
            "deprecated, a link SHOULD point to the latest version of the collection. The relation types "
            "`predecessor-version` (link to older version) and `successor-version` (link to newer version) "
            "can also be used to show the relation between versions.\n5. `alternate`: An alternative "
            "representation of the collection. For example, this could be the collection available through"
            "another catalog service such as OGC CSW, a human-readable HTML version or a metadata document"
            "following another standard such as ISO 19115 or DCAT. For additional relation types see also"
            "the lists of [common relation types in openEO](#section/API-Principles/Web-Linking) and the "
            "STAC specification for Collections."
        ),
    )
    cube_dimensions: Optional[dict[str, Dimension]] = Field(
        None,
        alias="cube:dimensions",
        description=(
            "Uniquely named dimensions of the data cube.\n\nThe keys of the object are the dimension names."
            "For interoperability, it is RECOMMENDED to use the\nfollowing dimension names if there is only "
            "a single dimension with the specified criteria:\n\n* `x` for the dimension of type `spatial` "
            "with the axis set to `x`\n* `y` for the dimension of type `spatial` with the axis set to `y`* "
            "`z` for the dimension of type `spatial` with the axis set to `z`\n* `t` for the dimension of "
            " type `temporal` * `bands` for dimensions of type `bands`\n\nThis property REQUIRES to add "
            "`datacube` to the list of `stac_extensions`."
        ),
        title="STAC Collection Cube Dimensions",
    )
    summaries: Optional[dict[str, Union[list[Any], CollectionSummaryStats]]] = Field(
        None,
        description=(
            "Collection properties from STAC extensions (e.g. EO,SAR, Satellite or Scientific) or even "
            "custom extensions.Summaries are either a unique set of all available\nvalues *or* "
            "statistics. Statistics by default only specify the range (minimum and maximum values), "
            "but can optionally be accompanied by additional statistical values. The range can specify"
            "the potential range of values, but it is recommended to be as precise as possible. The set "
            "of values MUST contain at least one element and it is strongly RECOMMENDED to list all values."
            "It is recommended to list as many properties as reasonable so that consumers get a full"
            "overview of the Collection. Properties that are covered by the Collection specification "
            "(e.g.\n`providers` and `license`) SHOULD NOT be repeated in the summaries.\n\nPotential "
            "fields for the summaries can be found here: **[STAC Common Metadata](https://github.com/radiantearth/stac-spec/blob/v1.0.0-rc.2/item-spec/common-metadata.md)**"  # noqa:E501
            "A list of commonly used fields throughout all domains **[Content Extensions](https://github.com/radiantearth/stac-spec/blob/v1.0.0-rc.2/extensions/README.md#list-of-content-extensions)**:"  # noqa:E501
            "Domain-specific fields for domains such as EO, SAR and point clouds.\n* **Custom Properties**:"
            "It is generally allowed to add custom fields."
        ),
        title="STAC Summaries (Collection Properties)",
    )
    assets: Optional[Any] = Field(
        None,
        description=(
            "Dictionary of asset objects for data that can be downloaded,\neach with a unique key."
            "The keys MAY be used by clients as file names.\n\nImplementing this property REQUIRES "
            "to add `collection-assets`\nto the list of `stac_extensions` in STAC < 1.0.0-rc.1."
        ),
    )

    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True


class Collections(TypedDict, total=False):
    collections: list[Collection]
    links: list[dict[str, Any]]


###########
# Processes
###########
class ProcessesGetResponse(BaseModel):
    processes: list[Process]
    links: list[Link]


class ProcessGraphWithMetadata(Process):
    id: str = Field(default=None, alias="id")
    summary: Optional[Any] = None
    description: Optional[Any] = None
    parameters: Optional[Any] = None
    returns: Optional[Any] = None
    process_graph: Any = None

    class Config:
        allow_population_by_field_name = True


class ProcessGraphsGetResponse(BaseModel):
    processes: list[ProcessGraphWithMetadata] = Field(
        ..., description="Array of user-defined processes"
    )
    links: list[Link]


class ValidationPostResponse(BaseModel):
    errors: list[Error] = Field(..., description="A list of validation errors.")


###########
# Jobs
###########
class BatchJob(BaseModel):
    job_id: uuid.UUID = Field(default=None, alias="id")
    title: Optional[str] = None
    description: Optional[str] = None
    process: Optional[ProcessGraphWithMetadata] = None
    status: Status
    progress: Optional[float] = Field(
        None,
        description="Indicates the process of a running batch job in percent.\nCan also be set for a job which stopped due to an error or was canceled by the user. In this case, the value indicates the progress at which the job stopped. The Property may not be available for the status codes `created` and `queued`.\nSubmitted and queued jobs only allow the value `0`, finished jobs only allow the value `100`.",
        example=75.5,
    )
    created: RFC3339Datetime
    updated: Optional[RFC3339Datetime] = None
    plan: Optional[str] = None
    costs: Optional[float] = None
    budget: Optional[float] = None
    usage: Optional[Usage] = Field(
        None,
        description="Metrics about the resource usage of the batch job.\n\nBack-ends are not expected to update the metrics while processing data,\nso the metrics can only be available after the job has been finished\nor has errored.\nFor usage metrics during processing, metrics can better be added to the\nlogs (e.g. `GET /jobs/{job_id}/logs`) with the same schema.",
    )

    @validator("job_id", pre=True, always=True)
    def as_str(cls, v):
        if isinstance(v, str):
            return v
        elif isinstance(v, uuid.UUID):
            return v.__str__()
        else:
            raise ValueError(f"Job id can only be of type UUID or str.")

    class Config:
        allow_population_by_field_name = True


class JobsGetResponse(BaseModel):
    jobs: list[BatchJob]
    links: list[Link]


class JobsGetLogsResponse(BaseModel):
    logs: list[Any]
    links: list[Link]


class JobsGetEstimateGetResponse(BaseModel):
    costs: Optional[float] = None
    duration: Optional[str] = Field(
        None,
        description="Estimated duration for the operation. Duration MUST be specified as a ISO 8601 duration.",
        example="P1Y2M10DT2H30M",
    )
    size: Optional[int] = Field(
        None,
        description="Estimated required storage capacity, i.e. the size of the generated files. Size MUST be specified in bytes.",
        example=157286400,
    )
    downloads_included: Optional[int] = Field(
        None,
        description="Specifies how many full downloads of the processed data are included in the estimate. Set to `null` for unlimited downloads, which is also the default value.",
        example=5,
    )
    expires: Optional[RFC3339Datetime] = Field(
        None,
        description="Time until which the estimate is valid, formatted as a [RFC 3339](https://www.rfc-editor.org/rfc/RFC3339Datetime.html) date-time.",
        example="2020-11-01T00:00:00Z",
    )


class FilesGetResponse(BaseModel):
    files: list[File]
    links: list[Link]


class FileFormatsGetResponse(BaseModel):
    input: dict[str, FileFormat] = Field(
        ...,
        description="Map of supported input file formats, i.e. file formats a back-end can **read** from. The property keys are the file format names that are used by clients and users, for example in process graphs.",
        title="Input File Formats",
    )
    output: dict[str, FileFormat] = Field(
        ...,
        description="Map of supported output file formats, i.e. file formats a back-end can **write** to. The property keys are the file format names that are used by clients and users, for example in process graphs.",
        title="Output File Formats",
    )


class MeGetResponse(BaseModel):
    user_id: uuid.UUID
    name: Optional[str] = Field(
        None,
        description="The user name, a human-friendly displayable name. Could be the user's real name or a nickname.",
    )
    default_plan: Optional[str] = Field(
        None,
        description="Name of the plan the user has subscribed to.\n\nOverrides the default plan of the back-end, but back-ends\nMAY also allow overriding this plan for each individual\nprocessing request (e.g. job or service) with the\ncorresponding `plan` property.",
        example="free",
    )
    storage: Optional[Storage1] = Field(
        None,
        description="Information about the storage space available to the user.",
        title="User Storage",
    )
    budget: Optional[float] = None
    links: Optional[list[Link]] = Field(
        None,
        description="Links related to the user profile, e.g. where payments\nare handled or the user profile could be edited.\n\nIt is RECOMMENDED to provide links with the following `rel` (relation) types:\n\n1. `payment`: A page where users can recharge their user account with money or credits.\n\n2. `edit-form`: Points to a page where the user can edit his user profile.\n\nFor additional relation types see also the lists of\n[common relation types in openEO](#section/API-Principles/Web-Linking).",
        example=[
            {"href": "https://example.openeo.org/john_doe/payment/", "rel": "payment"},
            {"href": "https://example.openeo.org/john_doe/edit/", "rel": "edit-form"},
            {
                "href": "https://example.openeo.org/john_doe/",
                "rel": "alternate",
                "type": "text/html",
                "title": "User profile",
            },
            {
                "href": "https://example.openeo.org/john_doe.vcf",
                "rel": "alternate",
                "type": "text/vcard",
                "title": "vCard of John Doe",
            },
        ],
    )


class UdfRuntimesGetResponse(BaseModel):
    pass

    class Config:
        extra = Extra.allow
