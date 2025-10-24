from enum import Enum


class TeamworkApplicationIdentityType(Enum):
    aadApplication = "0"
    bot = "1"
    tenantBot = "2"
    office365Connector = "3"
    outgoingWebhook = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkApplicationIdentityType"
