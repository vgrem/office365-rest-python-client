from typing import Dict, List, Optional, Union

from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.client_query import ClientQuery, T


class FunctionQuery(ClientQuery[T]):
    """Represents a function call OData query."""

    def __init__(
        self,
        binding_type: ClientObject,
        method_name: Optional[str] = None,
        method_params: Optional[Union[List, Dict, ClientValue]] = None,
        return_type: T = None,
    ) -> None:
        """Initialize a function query.

        Args:
            binding_type: The binding object type
            method_name: The name of the method to call
            method_params: Parameters for the method call
            return_type: The expected return type
        """
        super().__init__(binding_type.context, binding_type, None, None, return_type)
        self._path = ServiceOperationPath(
            method_name, method_params, binding_type.resource_path
        )

    def __repr__(self) -> str:
        return f"FunctionQuery(name={self.path.name})"

    @property
    def path(self) -> ServiceOperationPath:
        """Gets the service operation path for this function call."""
        return self._path

    @property
    def url(self) -> str:
        """Gets the full URL for the function call."""
        orig_url = super().url
        return f"{orig_url}/{self.path.segment}"

    @property
    def name(self) -> Optional[str]:
        """Gets the name of the method being called."""
        return self._path.name
