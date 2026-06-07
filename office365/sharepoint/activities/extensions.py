from office365.sharepoint.entity import Entity


class ActivityExtensions(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Activities.ActivityExtensions"
