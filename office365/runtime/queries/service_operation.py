from typing import AnyStr, Dict, List, Optional, Union

from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.client_query import ClientQuery, T


class ServiceOperationQuery(ClientQuery[T]):
    """Represents a service operation (function) call in OData.

    Can handle both static methods (class-level) and instance methods.
    """

    def __init__(
        self,
        binding_type: ClientObject,
        method_name: str = None,
        method_params: Optional[Union[List, Dict, ClientValue]] = None,
        parameters_type: Optional[Union[ClientObject, ClientValue, Dict, AnyStr]] = None,
        parameters_name: Optional[str] = None,
        return_type: Optional[T] = None,
        is_static: bool = False,
    ):
        super().__init__(
            binding_type.context,
            binding_type,
            parameters_type,
            parameters_name,
            return_type,
        )
        self._method_name = method_name
        self._method_params = method_params
        self.static = is_static

    def __repr__(self) -> str:
        return f"ServiceOperationQuery(name={self.path.name}, static={self.static}"

    @property
    def path(self) -> ServiceOperationPath:
        """Gets the service operation path for this query."""
        if self.static:
            static_name = f"{self.binding_type.entity_type_name}.{self._method_name}"
            return ServiceOperationPath(static_name, self._method_params)
        else:
            return ServiceOperationPath(self._method_name, self._method_params, self.binding_type.resource_path)

    @property
    def url(self) -> str:
        """Gets the full URL for the service operation call."""
        orig_url = super().url
        if self.static:
            return "".join([self.context.service_root_url, str(self.path)])
        else:
            return "/".join([orig_url, self.path.segment])

    @property
    def name(self) -> Optional[str]:
        """Gets the name of the method being called."""
        return self._method_name
