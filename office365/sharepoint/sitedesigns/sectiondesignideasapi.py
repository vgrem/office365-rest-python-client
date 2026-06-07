from office365.sharepoint.entity import Entity


class SectionDesignIdeasApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SectionDesignIdeas.SectionDesignIdeasApi"
