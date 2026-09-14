from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.logger.activityrequest import LogActivityRequest


class ActivityLogger(Entity):
    def log_activity(
        self, operation, list_id, list_item_unique_id, affected_resource_url, item_type, audit_creation_time, is_offline
    ):
        """Args:
        operation (str):
        list_id (str):
        list_item_unique_id (str):
        affected_resource_url (str):
        item_type (str):
        audit_creation_time (str):
        is_offline (bool):
        """
        payload = {
            "Operation": operation,
            "ListId": list_id,
            "ListItemUniqueId": list_item_unique_id,
            "AffectedResourceUrl": affected_resource_url,
            "ItemType": item_type,
            "AuditCreationTime": audit_creation_time,
            "IsOffline": is_offline,
        }
        qry = ServiceOperationQuery(self, "LogActivity", None, payload)
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ActivityLogger"

    def feedback_direct(
        self,
        operation: str,
        list_id: UUID,
        list_item_unique_id: UUID,
        affected_resource_url: str,
        item_type: str,
        json: str,
    ) -> Self:
        """FeedbackDirect operation.

        Args:
            operation (str): Operation parameter
            list_id (UUID): ListId parameter
            list_item_unique_id (UUID): ListItemUniqueId parameter
            affected_resource_url (str): AffectedResourceUrl parameter
            item_type (str): ItemType parameter
            json (str): json parameter
        """
        qry = ServiceOperationQuery(
            self,
            "FeedbackDirect",
            None,
            {
                "Operation": operation,
                "ListId": list_id,
                "ListItemUniqueId": list_item_unique_id,
                "AffectedResourceUrl": affected_resource_url,
                "ItemType": item_type,
                "json": json,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def feedback_indirect(
        self,
        operation: str,
        list_id: UUID,
        list_item_unique_id: UUID,
        affected_resource_url: str,
        item_type: str,
        json: str,
    ) -> Self:
        """FeedbackIndirect operation.

        Args:
            operation (str): Operation parameter
            list_id (UUID): ListId parameter
            list_item_unique_id (UUID): ListItemUniqueId parameter
            affected_resource_url (str): AffectedResourceUrl parameter
            item_type (str): ItemType parameter
            json (str): json parameter
        """
        qry = ServiceOperationQuery(
            self,
            "FeedbackIndirect",
            None,
            {
                "Operation": operation,
                "ListId": list_id,
                "ListItemUniqueId": list_item_unique_id,
                "AffectedResourceUrl": affected_resource_url,
                "ItemType": item_type,
                "json": json,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def log_activity_bulk(
        self,
        operation: str,
        site_id: UUID,
        web_id: UUID,
        list_id: UUID,
        mailbox_type: str,
        requests: ClientValueCollection[LogActivityRequest],
    ) -> Self:
        """LogActivityBulk operation.

        Args:
            operation (str): Operation parameter
            site_id (UUID): SiteId parameter
            web_id (UUID): WebId parameter
            list_id (UUID): ListId parameter
            mailbox_type (str): MailboxType parameter
            requests (ClientValueCollection[LogActivityRequest]): Requests parameter
        """
        qry = ServiceOperationQuery(
            self,
            "LogActivityBulk",
            None,
            {
                "Operation": operation,
                "SiteId": site_id,
                "WebId": web_id,
                "ListId": list_id,
                "MailboxType": mailbox_type,
                "Requests": requests,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
