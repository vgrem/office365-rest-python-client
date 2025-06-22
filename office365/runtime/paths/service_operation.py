from typing import Dict, List, Optional, Union

from office365.runtime.client_value import ClientValue
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath


class ServiceOperationPath(ResourcePath):
    """Represents a path to service operations (functions) in OData.

    Service operations represent simple functions exposed by an OData service that can be bound to a resource.
    """

    def __init__(
        self,
        name: str,
        parameters: Optional[Union[List, Dict, ClientValue]] = None,
        parent: Optional[ResourcePath] = None,
    ) -> None:
        """Initialize a service operation path.

        Args:
            name: The name of the service operation
            parameters: Parameters for the operation (list, dict, or ClientValue)
            parent: The parent resource path
        """
        super().__init__(name, parent)
        self._parameters = parameters

    @property
    def segment(self) -> str:
        """Gets the OData path segment for this service operation."""
        return ODataPathBuilder.build_segment(self)

    @property
    def name(self) -> str:
        """Gets the name of the service operation."""
        return self._key

    @property
    def parameters(self) -> Optional[Union[List, Dict, ClientValue]]:
        """Gets the parameters for the service operation."""
        return self._parameters
