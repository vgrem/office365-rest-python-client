from office365.runtime.client_value import ClientValue
from typing import Optional


class ColumnsInfo(ClientValue):
    def __init__(self, column_name: Optional[str] = None, view_field_name: Optional[str] = None):
        self.columnName = column_name
        self.viewFieldName = view_field_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.ColumnsInfo"
