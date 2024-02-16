"""Conformance Classes."""
from enum import Enum


class STACConformanceClasses(str, Enum):
    """STAC Api conformance classes."""

    CORE = "https://api.stacspec.org/v1.0.0/core"
    COLLECTIONS = "https://api.stacspec.org/v1.0.0/collections"


class OGCConformanceClasses(str, Enum):
    """OGC compliant conformance classes."""

    pass


BASIC_CONFORMANCE_CLASSES = [
    STACConformanceClasses.CORE,
    STACConformanceClasses.COLLECTIONS,
]
