from office365.sharepoint.entity import Entity


class RemoveExternalUsersResults(Entity):
    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantManagement.RemoveExternalUsersResults"
