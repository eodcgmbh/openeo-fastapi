"""Pydantic Models describing different api request and response bodies."""
import uuid
from enum import Enum
from typing import Any, List, Optional, TypedDict, Union

from pydantic import AnyUrl, BaseModel, Extra, Field, validator

from openeo_fastapi.api.types import (
    Billing,
    Dimension,
    Endpoint,
    Error,
    Extent,
    File,
    FileFormat,
    Link,
    Process,
    RFC3339Datetime,
    StacProvider,
    Status,
    Storage,
    Type5,
    Usage,
    Version,
)


###########
# Base
###########
class Capabilities(BaseModel):
    """Response model for GET (/)."""

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


class MeGetResponse(BaseModel):
    """Response model for GET (/me)."""

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
    storage: Optional[Storage] = Field(
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


class ConformanceGetResponse(BaseModel):
    """Response model for GET (/conformance)."""

    conformsTo: list[AnyUrl]


class WellKnownOpeneoGetResponse(BaseModel):
    """Response model for GET (/.well-known/openeo)."""

    versions: list[Version]


class UdfRuntimesGetResponse(BaseModel):
    """Response model for GET (/udf_runtimes)."""

    pass

    class Config:
        extra = Extra.allow


class GrantType(Enum):
    implicit = "implicit"
    authorization_code_pkce = "authorization_code+pkce"
    urn_ietf_params_oauth_grant_type_device_code_pkce = (
        "urn:ietf:params:oauth:grant-type:device_code+pkce"
    )
    refresh_token = "refresh_token"


class DefaultClient(BaseModel):
    id: str = Field(
        ...,
        description="The OpenID Connect Client ID to be used in the authentication procedure.",
    )
    grant_types: list[GrantType] = Field(
        ...,
        description="List of authorization grant types (flows) supported by the OpenID Connect client.\nA grant type descriptor consist of a OAuth 2.0 grant type,\nwith an additional `+pkce` suffix when the grant type should be used with\nthe PKCE extension as defined in [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636.html).\n\nAllowed values:\n- `implicit`: Implicit Grant as specified in [RFC 6749, sec. 1.3.2](https://www.rfc-editor.org/rfc/rfc6749.html#section-1.3.2)\n- `authorization_code+pkce`: Authorization Code Grant as specified in [RFC 6749, sec. 1.3.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-1.3.1), with PKCE extension.\n- `urn:ietf:params:oauth:grant-type:device_code+pkce`: Device Authorization Grant (aka Device Code Flow) as specified in [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628.html), with PKCE extension. Note that the combination of this grant with the PKCE extension is *not standardized* yet.\n- `refresh_token`: Refresh Token as specified in [RFC 6749, sec. 1.5](https://www.rfc-editor.org/rfc/rfc6749.html#section-1.5)",
    )
    redirect_urls: Optional[list[AnyUrl]] = Field(
        None,
        description="List of redirect URLs that are whitelisted by the OpenID Connect client.\nRedirect URLs MUST be provided when the OpenID Connect client supports\nthe `implicit` or `authorization_code+pkce` authorization flows.",
    )


class Provider(BaseModel):
    id: str = Field(
        ...,
        pattern=r"[\d\w]{1,20}",
        description="A **unique** identifier for the OpenID Connect Provider to be as prefix for the Bearer token.",
    )
    issuer: AnyUrl = Field(
        ...,
        description="The [issuer location](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) (also referred to as 'authority' in some client libraries) is the URL of the OpenID Connect provider, which conforms to a set of rules:\n1. After appending `/.well-known/openid-configuration` to the URL, a [HTTP/1.1 GET request](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationRequest) to the concatenated URL MUST return a [OpenID Connect Discovery Configuration Response](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse). The response provides all information required to authenticate using OpenID Connect.\n2. The URL MUST NOT contain a terminating forward slash `/`.",
        examples=["https://accounts.google.com"],
    )
    scopes: Optional[list[str]] = Field(
        None,
        description="A list of OpenID Connect scopes that the client MUST include when requesting authorization. If scopes are specified, the list MUST at least contain the `openid` scope.",
    )
    title: str = Field(
        ...,
        description="The name that is publicly shown in clients for this OpenID Connect provider.",
    )
    description: Optional[str] = Field(
        None,
        description="A description that explains how the authentication procedure works.\n\nIt should make clear how to register and get credentials. This should\ninclude instruction on setting up `client_id`, `client_secret` and `redirect_uri`.\n\n[CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich\ntext representation.",
    )
    default_clients: Optional[list[DefaultClient]] = Field(
        None,
        description='List of default OpenID Connect clients that can be used by an openEO client\nfor OpenID Connect based authentication.\n\nA default OpenID Connect client is managed by the backend implementer.\nIt MUST be configured to be usable without a client secret,\nwhich limits its applicability to OpenID Connect grant types like\n"Authorization Code Grant with PKCE" and "Device Authorization Grant with PKCE"\n\nA default OpenID Connect client is provided without availability guarantees.\nThe backend implementer CAN revoke, reset or update it any time.\nAs such, openEO clients SHOULD NOT store or cache default OpenID Connect client information\nfor long term usage.\nA default OpenID Connect client is intended to simplify authentication for novice users.\nFor production use cases, it is RECOMMENDED to set up a dedicated OpenID Connect client.',
        title="Default OpenID Connect Clients",
    )
    links: Optional[list[Link]] = Field(
        None,
        description="Links related to this provider, for example a\nhelp page or a page to register a new user account.\n\nFor relation types see the lists of\n[common relation types in openEO](#section/API-Principles/Web-Linking).",
    )


class CredentialsOidcGetResponse(BaseModel):
    providers: list[Provider] = Field(
        ...,
        description="The first provider in this list is the default provider for authentication. Clients can either pre-select or directly use the default provider for authentication if the user doesn't specify a specific value.",
    )


#############
# Collections
#############
class Collection(BaseModel):
    """Response model for GET (/collection/{collection_id})"""

    stac_version: str
    stac_extensions: Optional[list[Union[AnyUrl, str]]] = None
    type: str = Field(
        description="For STAC versions >= 1.0.0-rc.1 this field is required.",
        default="Collection",
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
    providers: Optional[list[StacProvider]] = None
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
    summaries: Optional[dict[str, Union[list[Any], Any]]] = Field(
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
    """Response model for GET (/collections)."""

    collections: list[Collection]
    links: list[dict[str, Any]]


###########
# Processes
###########
class ProcessesGetResponse(BaseModel):
    """Response model for GET (/processes)."""

    processes: list[Process]
    links: list[Link]


class ProcessGraphWithMetadata(Process):
    """Reponse model for
                GET (/process_graphs/{process_graph_id})

    Request model for
            PUT (/process_graphs/{process_graph_id})
            POST (/validation)
    """

    id: str = Field(default=None, alias="id")
    summary: Optional[Any] = None
    description: Optional[Any] = None
    parameters: Optional[Any] = None
    returns: Optional[Any] = None
    process_graph: Any = None

    class Config:
        allow_population_by_field_name = True


class ProcessGraphsGetResponse(BaseModel):
    """Response model for GET (/process_graphs)."""

    processes: list[ProcessGraphWithMetadata] = Field(
        ..., description="Array of user-defined processes"
    )
    links: list[Link]


class ValidationPostResponse(BaseModel):
    """Response model for POST (/validation)."""

    errors: list[Error] = Field(..., description="A list of validation errors.")


###########
# Jobs
###########
class BatchJob(BaseModel):
    """Reponse model for GET (/jobs/{job_id})."""

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
    """Reponse model for GET (/jobs)."""

    jobs: list[BatchJob]
    links: list[Link]


class JobsGetLogsResponse(BaseModel):
    """Reponse model for GET (/jobs/{job_id}/logs)."""

    logs: list[Any]
    links: list[Link]


class JobsGetEstimateGetResponse(BaseModel):
    """Reponse model for GET (/jobs/{job_id}/estimate)."""

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


class JobsRequest(BaseModel):
    """Request model for
    POST (/jobs)
    PATCH (/jobs/{job_id})
    POST (/result)
    """

    title: str = None
    description: Optional[str] = None
    process: Optional[ProcessGraphWithMetadata] = None
    plan: Optional[str] = None
    budget: Optional[str] = None


###########
# Files
###########
class FilesGetResponse(BaseModel):
    """Reponse model for GET (/files)."""

    files: list[File]
    links: list[Link]


class FileFormatsGetResponse(BaseModel):
    """Reponse model for GET (/file_formats)."""

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
