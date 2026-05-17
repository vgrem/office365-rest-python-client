from office365.runtime.client_value import ClientValue


class CollaborativeUsers(ClientValue):
    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeUsers"
