from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, cast

from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.client_query import ClientQuery, ReturnT

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.odata.query_options import QueryOptions


class ReadEntityQuery(ClientQuery[ReturnT]):
    def __init__(self, return_type: ClientObject, properties_to_include: Optional[List[str]] = None) -> None:
        """
        Read client object query
        """
        super().__init__(return_type.context, return_type, None, None, return_type)  # type: ignore[reportArgumentType]
        self._query_options: Optional["QueryOptions"] = None
        self._properties_to_include = properties_to_include

    @property
    def query_options(self) -> "QueryOptions":
        if self._query_options is None:
            self._query_options = self._build_query_options()
        return self._query_options

    def _build_query_options(self) -> "QueryOptions":
        """Resolve query options for the return object, expanding the requested properties."""
        from office365.runtime.client_object import ClientObject
        from office365.runtime.client_object_collection import ClientObjectCollection

        client_object = cast(ClientObject, self._return_type)
        query_options = client_object.query_options
        for name in self._properties_to_include or []:
            if name in query_options.select:
                continue

            if isinstance(client_object, ClientObjectCollection):
                prop = client_object.create_typed_object().get_property(name)
            else:
                prop = client_object.get_property(name)

            if name == "Properties" or isinstance(prop, ClientObject):
                query_options.expand.append(name)
            query_options.select.append(name)
        return query_options

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
