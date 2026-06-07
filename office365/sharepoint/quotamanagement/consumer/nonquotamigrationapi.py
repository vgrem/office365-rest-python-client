from office365.sharepoint.entity import Entity


class NonQuotaMigrationApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.QuotaManagement.Consumer.NonQuotaMigrationApi"
