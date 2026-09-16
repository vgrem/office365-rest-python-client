from office365.sharepoint.entity import Entity


class MigrationTaskEntityData(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskEntityData"
