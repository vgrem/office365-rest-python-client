from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.comments.comment import Comment
from office365.sharepoint.entity_collection import EntityCollection


class CommentCollection(EntityCollection[Comment]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, Comment, resource_path)

    def delete_all(self) -> ClientResult[bool]:
        """Deletes all the comments."""
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "DeleteAll", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type
