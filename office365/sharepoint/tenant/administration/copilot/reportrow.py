from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ReportRow(ClientValue):
    def __init__(self, row: StringCollection = StringCollection()):
        self.Row = row

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportRow"
