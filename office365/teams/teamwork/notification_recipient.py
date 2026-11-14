from office365.runtime.client_value import ClientValue


class TeamworkNotificationRecipient(ClientValue):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkNotificationRecipient"
