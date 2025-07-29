from office365.runtime.client_value import ClientValue


class ActivityCapabilities(ClientValue):
    """ """
    def __init__(
        self,
        client_activities_enabled: bool = None,
        client_activities_notification_enabled: bool = None,
        enabled: bool = None,
    ) -> None:
        """ """
        self.clientActivitiesEnabled = client_activities_enabled
        self.clientActivitiesNotificationEnabled = (
            client_activities_notification_enabled
        )
        self.enabled = enabled

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityCapabilities"
