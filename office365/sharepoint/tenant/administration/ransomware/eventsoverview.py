from office365.runtime.client_value import ClientValue


class TenantAdminRansomwareEventsOverview(ClientValue):
    def __init__(self, active_events_count: int = None, open_events_count: int = None):
        self.activeEventsCount = active_events_count
        self.openEventsCount = open_events_count

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEventsOverview"
