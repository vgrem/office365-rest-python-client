from __future__ import annotations

from typing import List

from typing_extensions import Self

from office365.entity import Entity
from office365.onedrive.workbooks.sort_field import WorkbookSortField
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery


class WorkbookTableSort(Entity):
    """Manages sorting operations on Table objects."""

    def apply(
        self,
        fields: List[WorkbookSortField],
        match_case: bool | None = None,
        method: str | None = None,
    ) -> Self:
        """Perform a sort operation.

        Args:
            fields (list[WorkbookSortField]): The list of conditions to sort on.
            match_case (bool): Indicates whether to match the case of the items being sorted.
            method (str): The ordering method used for Chinese characters. The possible values are: PinYin, StrokeCount.
        """
        payload = {
            "fields": ClientValueCollection(WorkbookSortField, fields),
            "matchCase": match_case,
            "method": method,
        }
        qry = ServiceOperationQuery(self, "apply", None, payload)
        self.context.add_query(qry)
        return self
