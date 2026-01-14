from office365.runtime.client_value import ClientValue


class ColumnsInfo(ClientValue):
    def __init__(self, column_name: str = None, view_field_name: str = None):
        self.columnName = column_name
        self.viewFieldName = view_field_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.ColumnsInfo"
