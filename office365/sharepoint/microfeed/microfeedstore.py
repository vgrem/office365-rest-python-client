from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class MicrofeedStore(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Microfeed.MicrofeedStore"

    def add_data(self, name: str, data: bytes) -> Self:
        """AddData operation.

        Args:
            name (str): name parameter
            data (bytes): data parameter
        """
        qry = ServiceOperationQuery(self, "AddData", None, {"name": name, "data": data}, None, None)
        self.context.add_query(qry)
        return self

    def add_data_as_stream(self, name: str, data: bytes) -> Self:
        """AddDataAsStream operation.

        Args:
            name (str): name parameter
            data (bytes): data parameter
        """
        qry = ServiceOperationQuery(self, "AddDataAsStream", None, {"name": name, "data": data}, None, None)
        self.context.add_query(qry)
        return self

    def execute_pending_operations(self) -> Self:
        """ExecutePendingOperations operation."""
        qry = ServiceOperationQuery(self, "ExecutePendingOperations", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def get_social_properties(self, account_name: str) -> ClientResult[str]:
        """GetSocialProperties operation.

        Args:
            account_name (str): accountName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetSocialProperties", None, {"accountName": account_name}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def increment_unread_at_mention_count(self, account_name: str) -> Self:
        """IncrementUnreadAtMentionCount operation.

        Args:
            account_name (str): accountName parameter
        """
        qry = ServiceOperationQuery(
            self, "IncrementUnreadAtMentionCount", None, {"accountName": account_name}, None, None
        )
        self.context.add_query(qry)
        return self

    def set_post_like_status(self, account_name: str, post_id: str, like: bool) -> Self:
        """SetPostLikeStatus operation.

        Args:
            account_name (str): accountName parameter
            post_id (str): postId parameter
            like (bool): like parameter
        """
        qry = ServiceOperationQuery(
            self, "SetPostLikeStatus", None, {"accountName": account_name, "postId": post_id, "like": like}, None, None
        )
        self.context.add_query(qry)
        return self
