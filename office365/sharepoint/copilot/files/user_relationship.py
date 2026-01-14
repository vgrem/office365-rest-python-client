from datetime import datetime

from office365.runtime.client_value import ClientValue


class CopilotFileUserRelationship(ClientValue):
    def __init__(self, last_access_date_time: datetime = None):
        self.LastAccessDateTime = last_access_date_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotFileUserRelationship"
