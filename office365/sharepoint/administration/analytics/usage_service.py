from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SPAnalyticsUsageService(Entity):
    """Represents the entry point for the Event REST service exposed through CSOM"""

    def __init__(self, context):
        static_path = ResourcePath("Microsoft.SharePoint.Administration.SPAnalyticsUsageService")
        super().__init__(context, static_path)

    def log_event(self, event_type_id, scope_id, item_id, site=None, user=None):
        """Used to log events.

        Args:
            event_type_id (int): Specifies the type of an analytics event
            scope_id (str):
            item_id (str):
            site (str):
            user (str):
        """
        payload = {
            "EventTypeId": event_type_id,
            "ItemId": item_id,
            "ScopeId": scope_id,
            "Site": site,
            "User": user,
        }
        qry = ServiceOperationQuery(self, "logevent", None, payload)
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.SPAnalyticsUsageService"
