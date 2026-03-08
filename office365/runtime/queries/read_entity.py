from __future__ import annotations

from typing import TYPE_CHECKING, List

from office365.runtime.queries.client_query import ClientQuery, T

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.odata.query_options import QueryOptions


class ReadEntityQuery(ClientQuery[T]):
    def __init__(self, return_type: ClientObject, properties_to_include: List[str] | None = None) -> None:
        """
        Read client object query
        """
        super().__init__(return_type.context, return_type, None, None, return_type)
        self._query_options = None
        self._properties_to_include = properties_to_include

    @property
    def query_options(self) -> QueryOptions:
        from office365.runtime.odata.query_options import QueryOptions
        from office365.runtime.odata.query_options_builder import QueryOptionsBuilder

        if self._query_options is None:
            self._query_options = QueryOptionsBuilder.build(self._return_type, self._properties_to_include)
        return self._query_options

    @property
    def url(self) -> str:
        if self.query_options.is_empty:
            return self.binding_type.resource_url or ""

        delimiter = "?"
        from office365.runtime.client_value import ClientValue
        from office365.runtime.paths.service_operation import ServiceOperationPath

        if isinstance(self.path, ServiceOperationPath) and isinstance(self.path.parameters, ClientValue):
            delimiter = "&"
        return self.binding_type.resource_url + delimiter + str(self.query_options)
