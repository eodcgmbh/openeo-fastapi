from enum import Enum
from typing import Any, Optional, TypedDict, Union

from pydantic import AnyUrl, BaseModel, Extra, Field

from openeo_fastapi.client.models import Link, Type1, Type2


class CollectionId(str):
    collection_id = Field(
        ...,
        description="A unique identifier for the collection, which MUST match the specified pattern.",
        example="Sentinel-2A",
    )


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


class Description(BaseModel):
    __root__: str = Field(
        ...,
        description="""Detailed description to explain the entity.
        [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation.""",
    )


class Dimension(BaseModel):
    type: Type2 = Field(..., description="Type of the dimension.")
    description: Optional[Description] = None


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


class IntervalItem(BaseModel):
    __root__: list[Any] = Field(
        ...,
        description=(
            "Begin and end times of the time interval. The coordinate reference system is the "
            "Gregorian calendar.\n\nThe value `null` is supported and indicates an open time interval."
        ),
        example=["2011-11-11T12:22:11Z", None],
    )


class Temporal(BaseModel):
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


class StacLicense(BaseModel):
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
