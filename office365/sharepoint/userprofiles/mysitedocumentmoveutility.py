from office365.sharepoint.entity import Entity


class MySiteDocumentMoveUtility(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Portal.UserProfiles.MySiteDocumentMoveUtility"
