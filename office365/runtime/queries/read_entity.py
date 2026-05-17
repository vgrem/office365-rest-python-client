from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.client_query import ClientQuery, T

if TYPE_CHECKING:
    from office365.runtime.odata.query_options import QueryOptions


class ReadEntityQuery(ClientQuery[T]):
    def __init__(self, return_type: ClientObject, properties_to_include: Optional[List[str]] = None) -> None:
        """
        Read client object query
        """
        super().__init__(return_type.context, return_type, None, None, return_type)  # type: ignore[reportArgumentType]
        self._query_options: Optional["QueryOptions"] = None
        self._properties_to_include = properties_to_include

    @property
    def query_options(self) -> "QueryOptions":
        from office365.runtime.odata.query_options_builder import QueryOptionsBuilder

        if self._query_options is None:
            self._query_options = QueryOptionsBuilder.build(self._return_type, self._properties_to_include)  # type: ignore[reportArgumentType]
        return self._query_options

    @property
    def url(self) -> str:
        assert self.binding_type is not None
        if self.query_options.is_empty:
            return self.binding_type.resource_url or ""

        delimiter = "?"

        if isinstance(self.path, ServiceOperationPath) and isinstance(self.path.parameters, ClientValue):
            delimiter = "&"
        resource_url = self.binding_type.resource_url
        assert resource_url is not None
        return resource_url + delimiter + str(self.query_options)
