from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.onedrive.workbooks.sort_field import WorkbookSortField


class WorkbookRangeSort(Entity):
    """Manages sorting operations on Range objects."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookRangeSort"

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def apply(
        self,
        fields: ClientValueCollection[WorkbookSortField],
        match_case: bool,
        has_headers: bool,
        orientation: str,
        method: str,
    ) -> Self:
        """apply operation.

        Args:
            fields (ClientValueCollection[WorkbookSortField]):
                fields parameter
            match_case (bool):
                matchCase parameter
            has_headers (bool):
                hasHeaders parameter
            orientation (str):
                orientation parameter
            method (str):
                method parameter
        """
        qry = ServiceOperationQuery(
            self,
            "apply",
            None,
            {
                "fields": fields,
                "matchCase": match_case,
                "hasHeaders": has_headers,
                "orientation": orientation,
                "method": method,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
