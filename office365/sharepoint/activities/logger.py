from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class ActivityLogger(Entity):
    def log_activity(
        self,
        operation,
        list_id,
        list_item_unique_id,
        affected_resource_url,
        item_type,
        audit_creation_time,
        is_offline,
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
