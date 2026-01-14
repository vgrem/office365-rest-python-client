from enum import Enum


class ODataV3MetadataLevel(str, Enum):
    """Defines the amount of metadata information to include in OData v3 responses.

    These values control how much control information is included in the payload
    when making OData v3 requests. The level affects both client and server behavior.

    Usage:
        >>> headers = {"Accept": f"application/json;odata={ODataV3MetadataLevel.MinimalMetadata}"}
    """

    Verbose = "verbose"
    """Indicates that the service MUST include all control information explicitly in the payload."""

    NoMetadata = "nometadata"
    """Indicates that the service SHOULD omit control information other than odata.nextLink and odata.count"""

    MinimalMetadata = "minimalmetadata"
    """Indicates that the service SHOULD remove computable control information from the payload wherever possible"""
