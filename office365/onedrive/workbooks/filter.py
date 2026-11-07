from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.onedrive.workbooks.filter_criteria import WorkbookFilterCriteria
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onedrive.workbooks.icon import WorkbookIcon
    from office365.runtime.types.json import Json


class WorkbookFilter(Entity):
    """Manages the filtering of a table's column."""

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def apply_bottom_items_filter(self, count: int | None = None) -> Self:
        """Perform a sort operation.

        Args:
            count (int): The number of items to apply the filter to.
        """
        payload = {"count": count}
        qry = ServiceOperationQuery(self, "applyBottomItemsFilter", None, payload)
        self.context.add_query(qry)
        return self

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def clear(self) -> Self:
        """Clear the filter on the given column."""
        qry = ServiceOperationQuery(self, "clear")
        self.context.add_query(qry)
        return self

    @odata(name="criteria")
    @property
    def criteria(self) -> Optional[WorkbookFilterCriteria]:
        """The currently applied filter on the given column."""
        return self.properties.get("criteria", WorkbookFilterCriteria())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookFilter"

    def apply(self, criteria: WorkbookFilterCriteria) -> Self:
        """apply operation.

        Args:
            criteria (WorkbookFilterCriteria):
                criteria parameter
        """
        qry = ServiceOperationQuery(self, "apply", None, {"criteria": criteria}, None, None)
        self.context.add_query(qry)
        return self

    def apply_bottom_percent_filter(self, percent: int) -> Self:
        """applyBottomPercentFilter operation.

        Args:
            percent (int):
                percent parameter
        """
        qry = ServiceOperationQuery(self, "applyBottomPercentFilter", None, {"percent": percent}, None, None)
        self.context.add_query(qry)
        return self

    def apply_cell_color_filter(self, color: str) -> Self:
        """applyCellColorFilter operation.

        Args:
            color (str):
                color parameter
        """
        qry = ServiceOperationQuery(self, "applyCellColorFilter", None, {"color": color}, None, None)
        self.context.add_query(qry)
        return self

    def apply_custom_filter(self, criteria1: str, criteria2: str, oper: str) -> Self:
        """applyCustomFilter operation.

        Args:
            criteria1 (str):
                criteria1 parameter
            criteria2 (str):
                criteria2 parameter
            oper (str):
                oper parameter
        """
        qry = ServiceOperationQuery(
            self, "applyCustomFilter", None, {"criteria1": criteria1, "criteria2": criteria2, "oper": oper}, None, None
        )
        self.context.add_query(qry)
        return self

    def apply_dynamic_filter(self, criteria: str) -> Self:
        """applyDynamicFilter operation.

        Args:
            criteria (str):
                criteria parameter
        """
        qry = ServiceOperationQuery(self, "applyDynamicFilter", None, {"criteria": criteria}, None, None)
        self.context.add_query(qry)
        return self

    def apply_font_color_filter(self, color: str) -> Self:
        """applyFontColorFilter operation.

        Args:
            color (str):
                color parameter
        """
        qry = ServiceOperationQuery(self, "applyFontColorFilter", None, {"color": color}, None, None)
        self.context.add_query(qry)
        return self

    def apply_icon_filter(self, icon: WorkbookIcon) -> Self:
        """applyIconFilter operation.

        Args:
            icon (WorkbookIcon):
                icon parameter
        """
        qry = ServiceOperationQuery(self, "applyIconFilter", None, {"icon": icon}, None, None)
        self.context.add_query(qry)
        return self

    def apply_top_items_filter(self, count: int) -> Self:
        """applyTopItemsFilter operation.

        Args:
            count (int):
                count parameter
        """
        qry = ServiceOperationQuery(self, "applyTopItemsFilter", None, {"count": count}, None, None)
        self.context.add_query(qry)
        return self

    def apply_top_percent_filter(self, percent: int) -> Self:
        """applyTopPercentFilter operation.

        Args:
            percent (int):
                percent parameter
        """
        qry = ServiceOperationQuery(self, "applyTopPercentFilter", None, {"percent": percent}, None, None)
        self.context.add_query(qry)
        return self

    def apply_values_filter(self, values: Json) -> Self:
        """applyValuesFilter operation.

        Args:
            values (Json):
                values parameter
        """
        qry = ServiceOperationQuery(self, "applyValuesFilter", None, {"values": values}, None, None)
        self.context.add_query(qry)
        return self
