from office365.sharepoint.entity import Entity


class LikesAPI(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Likes.LikesAPI"
