from office365.sharepoint.entity import Entity


class CommentsAPI(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Comments.CommentsAPI"
