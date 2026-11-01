from office365.entity_collection import EntityCollection
from office365.onedrive.workbooks.tables.pivot_table import WorkbookPivotTable
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery


class WorkbookPivotTableCollection(EntityCollection[WorkbookPivotTable]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, WorkbookPivotTable, resource_path)

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def refresh_all(self):
        """Refreshes the PivotTable."""
        qry = ServiceOperationQuery(self, "refreshAll")
        self.context.add_query(qry)
        return self
