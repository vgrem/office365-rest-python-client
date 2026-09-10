from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.client_query import ClientQuery, ReturnT

if TYPE_CHECKING:
    from office365.runtime.odata.query_options import QueryOptions


class FunctionQuery(ClientQuery[ReturnT]):
    """Represents a function call OData query."""

    def __init__(
        self,
        binding_type: ClientObject,
        method_name: str | None = None,
        method_params: list | dict | ClientValue | None = None,
        return_type: ReturnT | None = None,
        return_raw_content: bool = False,
    ) -> None:
        """Initialize a function query.

        Args:
            binding_type: The binding object type
            method_name: The name of the method to call
            method_params: Parameters for the method call
            return_type: The expected return type
            return_raw_content: When True, the response body is treated as raw content
                (e.g. file download) rather than parsed as OData JSON.
        """
        super().__init__(binding_type.context, binding_type, None, None, return_type)
        self._path = ServiceOperationPath(method_name or "", method_params, binding_type.resource_path)
        self._return_raw_content = return_raw_content

    @property
    def return_raw_content(self) -> bool:
        """Whether the response should be treated as raw content, not OData JSON."""
        return self._return_raw_content

    @property
    def query_options(self) -> Optional["QueryOptions"]:
        """Query options carried by the function's return collection (if any)."""
        return self._return_type.query_options if isinstance(self._return_type, ClientObject) else None

    @property
    def url(self) -> str:
        """The function URL with any fluent query options appended.

        Function endpoints (e.g. ``getAllMessages``) accept standard OData query
        options, so ``.filter()/.select()/.top()`` set on the returned
        collection are forwarded to the request.
        """
        url = super().url
        options = self.query_options
        if options is not None and not options.is_empty:
            delimiter = "&" if "?" in url else "?"
            url = f"{url}{delimiter}{options}"
        return url

    def __repr__(self):
        return f"FunctionQuery(name={self.name})"

    @property
    def path(self) -> ServiceOperationPath:
        """Gets the service operation path for this function call."""
        return self._path

    @property
    def name(self) -> str | None:
        """Gets the name of the method being called."""
        return self._path.name
