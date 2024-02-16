
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, BaseModel, Extra, Field, constr

# Avoids a Pydantic error:
# TypeError: You should use `typing_extensions.TypedDict` instead of
# `typing.TypedDict` with Python < 3.9.2.  Without it, there is no way to
# differentiate required and optional fields when subclassed.
if sys.version_info < (3, 9, 2):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class Type1(Enum):
    Collection = "Collection"


class Type2(Enum):
    spatial = "spatial"
    temporal = "temporal"
    bands = "bands"
    other = "other"



class Type5(Enum):
    Catalog = "Catalog"


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


class StacVersion(BaseModel):
    __root__: constr(regex=r"^(0\.9.\d+|1\.\d+.\d+)") = Field(
        ...,
        description="The [version of the STAC specification](https://github.com/radiantearth/stac-spec/releases), which MAY not be equal to the [STAC API version](#section/STAC). Supports versions 0.9.x and 1.x.x.",
    )


class Production(BaseModel):
    __root__: bool = Field(
        ...,
        description="Specifies whether the implementation is ready to be used in production use (`true`) or not (`false`).\nClients SHOULD only connect to non-production implementations if the user explicitly confirmed to use a non-production implementation.\nThis flag is part of `GET /.well-known/openeo` and `GET /`. It MUST be used consistently in both endpoints.",
    )


class Method(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


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
    stac_version: StacVersion
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
    production: Optional[Production] = None
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

      
class CollectionId(str):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    collection_id: constr(regex=rb"^[\w\-\.~\/]+$") = Field(
        ...,
        description="A unique identifier for the collection, which MUST match the specified pattern.",
        example="Sentinel-2A",
    )


class StacExtensions(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: list[Union[AnyUrl, str]] = Field(
        ...,
        description=(
            "A list of implemented STAC extensions. The list contains URLs to the JSON Schema "
            "files it can be validated against. For STAC < 1.0.0-rc.1  shortcuts such as `sar` "
            "can be used instead of the schema URL."
        ),
        unique_items=True,
    )


class StacAssets(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    pass

    class Config:
        extra = Extra.allow


class Role(Enum):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    producer = "producer"
    licensor = "licensor"
    processor = "processor"
    host = "host"


class StacProvider(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

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
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: list[StacProvider] = Field(
        ...,
        description=(
            "A list of providers, which MAY include all organizations capturing or processing "
            "the data or the hosting provider. Providers SHOULD be listed in chronological order"
            "with the most recent provider being the last element of the list."
        ),
    )


class Description(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: str = Field(
        ...,
        description="""Detailed description to explain the entity.
        [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation.""",
    )


class Dimension(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    type: Type2 = Field(..., description="Type of the dimension.")
    description: Optional[Description] = None


class Spatial(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

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


class IntervalItem(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: list[Any] = Field(
        ...,
        description=(
            "Begin and end times of the time interval. The coordinate reference system is the "
            "Gregorian calendar.\n\nThe value `null` is supported and indicates an open time interval."
        ),
        example=["2011-11-11T12:22:11Z", None],
    )


class Temporal(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    interval: Optional[list[IntervalItem]] = Field(
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
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

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
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    min: Union[str, float] = Field(alias="minimum")
    max: Union[str, float] = Field(alias="maximum")


class StacLicense(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: str = Field(
        ...,
        description=(
            "License(s) of the data as a SPDX [License identifier](https://spdx.org/licenses/)."
            "Alternatively, use `proprietary` if the license is not on the SPDX\nlicense list or"
            "`various` if multiple licenses apply. In these two cases\nlinks to the license texts "
            "SHOULD be added, see the `license` link\nrelation type.\n\nNon-SPDX licenses SHOULD "
            "add a link to the license text with the\n`license` relation in the links section. "
            "The license text MUST NOT be\nprovided as a value of this field. If there is no public"
            "license URL\navailable, it is RECOMMENDED to host the license text and link to it."
        ),
        example="Apache-2.0",
    )


class Collection(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    stac_version: StacVersion
    stac_extensions: Optional[StacExtensions] = None
    type: Optional[Type1] = Field(
        None, description="For STAC versions >= 1.0.0-rc.1 this field is required."
    )
    id: CollectionId
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
    license: StacLicense
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
    assets: Optional[StacAssets] = Field(
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


class LinksPagination(BaseModel):
    """
    Based on https://github.com/stac-utils/stac-fastapi/tree/main/stac_fastapi/types/stac_fastapi/types
    """

    __root__: list[Link] = Field(
        ...,
        description="""Links related to this list of resources, for example links for pagination\nor
        alternative formats such as a human-readable HTML version.\nThe links array MUST NOT be paginated.
        If pagination is implemented, the following `rel` (relation) types apply:\n\n1. `next` (REQUIRED):
        A link to the next page, except on the last page.\n\n2. `prev` (OPTIONAL): A link to the previous
        page, except on the first page.\n\n3. `first` (OPTIONAL): A link to the first page, except on the
        first page.\n\n4. `last` (OPTIONAL): A link to the last page, except on the last page.\n\nFor
        additional relation types see also the lists of
        [common relation types in openEO](#section/API-Principles/Web-Linking).""",
    )


class Collections(TypedDict, total=False):
    """
    All collections endpoint.
    https://github.com/radiantearth/stac-api-spec/tree/master/collections
    """

    collections: list[Collection]
    links: list[dict[str, Any]]

class ConformanceGetResponse(BaseModel):
    conformsTo: list[AnyUrl]


class Version(BaseModel):
    url: AnyUrl = Field(
        ...,
        description="*Absolute* URLs to the service.",
        example="https://example.com/api/v1.0",
    )
    production: Optional[Production] = None
    api_version: str = Field(
        ...,
        description="Version number of the openEO specification this back-end implements.",
    )


class WellKnownOpeneoGetResponse(BaseModel):
    versions: list[Version]

