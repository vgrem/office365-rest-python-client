from office365.sharepoint.entity import Entity


class SPVivaLearningManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.Claims.SPVivaLearningManager"
