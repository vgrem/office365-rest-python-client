from office365.sharepoint.entity import Entity


class DeleteTargetSiteEntity(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DeleteTargetSiteEntity"
