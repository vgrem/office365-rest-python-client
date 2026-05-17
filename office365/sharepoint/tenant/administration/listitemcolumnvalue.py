from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantAdminListItemColumnValue(ClientValue):
    def __init__(self, column_name: Optional[str] = None, column_value: Optional[str] = None):
        self.columnName = column_name
        self.columnValue = column_value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminListItemColumnValue"
