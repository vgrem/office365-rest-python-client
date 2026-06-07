from office365.sharepoint.entity import Entity


class UserActionAPI(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.UserActions.UserActionAPI"
