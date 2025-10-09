from office365.runtime.client_value import ClientValue


class TenantAdminListItemColumnValue(ClientValue):

    def __init__(self, column_name: str = None, column_value: str = None):
        self.columnName = column_name
        self.columnValue = column_value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminListItemColumnValue"
