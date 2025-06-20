from abc import ABC, abstractmethod

from office365.runtime.odata.v3.metadata_level import ODataV3MetadataLevel


class ODataJsonFormat(ABC):
    """
    Abstract base class defining the OData JSON format specification.

    This class serves as a contract for concrete OData JSON format implementations,
    ensuring they provide all required format properties and metadata handling.
    """

    def __init__(self, metadata_level: ODataV3MetadataLevel = None):
        """
        Initialize the OData JSON format handler.

        Args:
            metadata_level: The level of metadata to include in responses.
                           Typical values are 'none', 'minimal', and 'full'.
                           Defaults to None which typically implies server defaults.
        """
        self.metadata_level = metadata_level

    @property
    @abstractmethod
    def metadata_type(self) -> str:
        """The type identifier used for metadata in the JSON payload"""
        raise NotImplementedError

    @property
    @abstractmethod
    def collection(self) -> str:
        """The JSON property name used for collections/set of entities"""
        raise NotImplementedError

    @property
    @abstractmethod
    def collection_next(self) -> str:
        """str: The JSON property name used for next page links in collections"""
        raise NotImplementedError

    @property
    @abstractmethod
    def collection_delta(self) -> str:
        """str: The JSON property name used for delta/differential updates"""
        raise NotImplementedError

    @property
    @abstractmethod
    def etag(self) -> str:
        """str: The JSON property name used for entity tags (concurrency control)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def value_tag(self) -> str:
        """str: The JSON property name used for primitive value wrappers"""
        raise NotImplementedError

    @property
    @abstractmethod
    def media_type(self) -> str:
        """str: Gets the official media type for this format (e.g., 'application/json')"""
        raise NotImplementedError

    @property
    @abstractmethod
    def include_control_information(self) -> bool:
        """
        bool: Determines whether control information should be included in payload

        Control information includes annotations and other OData-specific metadata
        that guides client behavior but isn't part of the actual entity data.
        """
        raise NotImplementedError
