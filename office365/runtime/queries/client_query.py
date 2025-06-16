from __future__ import annotations

from typing import TYPE_CHECKING, AnyStr, Dict, Generic, Optional, TypeVar, Union

from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_result import ClientResult
    from office365.runtime.client_runtime_context import ClientRuntimeContext
    from office365.runtime.client_value import ClientValue

T = TypeVar("T", bound=Union["ClientObject", "ClientResult"])


class ClientQuery(Generic[T]):
    """Client query"""

    def __init__(
        self,
        context: ClientRuntimeContext,
        binding_type: Optional[ClientObject] = None,
        parameters_type: Optional[
            Union[ClientObject, ClientValue, Dict, AnyStr]
        ] = None,
        parameters_name: Optional[str] = None,
        return_type: Optional[T] = None,
    ) -> None:
        """
        Initialize a client query

        Args:
            context: The client runtime context
            binding_type: The object this query is bound to (optional)
            parameters_type: Type of parameters (ClientObject, ClientValue, dict, or string)
            parameters_name: Name of the parameters collection (optional)
            return_type: Expected return type of the query (optional)
        """
        self._context = context
        self._binding_type = binding_type
        self._parameters_type = parameters_type
        self._parameters_name = parameters_name
        self._return_type = return_type

    def build_request(self) -> RequestOptions:
        """Builds a request"""
        return self.context.build_request(self)

    def execute_query(self) -> T:
        """Executes the query and returns the result.

        Returns:
            The query result of type T

        Raises:
            ClientRequestException: If query execution fails
        """
        self.context.execute_query()
        return self.return_type

    @property
    def url(self) -> str:
        if self.binding_type is not None:
            return self.binding_type.resource_url
        else:
            return self.context.service_root_url

    @property
    def query_options(self):
        return self.binding_type.query_options

    @property
    def path(self) -> Optional[ResourcePath]:
        """The resource path for this query.

        Returns:
            ResourcePath of the bound object or None
        """
        if self.binding_type is not None:
            return self.binding_type.resource_path
        else:
            return None

    @property
    def context(self) -> ClientRuntimeContext:
        """The client runtime context."""
        return self._context

    @property
    def id(self) -> int:
        """The unique identifier of the query."""
        return id(self)

    @property
    def binding_type(self):
        """The object this query is bound to."""
        return self._binding_type

    @property
    def parameters_name(self) -> Optional[str]:
        """Name of the parameters collection."""
        return self._parameters_name

    @property
    def parameters_type(self):
        """Type of parameters for this query."""
        return self._parameters_type

    @property
    def return_type(self) -> Optional[T]:
        """Expected return type of this query."""
        return self._return_type
