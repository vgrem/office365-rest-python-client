from office365.runtime.client_value import ClientValue


class AnnouncementAction(ClientValue):

    def __init__(self, type_: str = None, value: bool = None):
        self.Type = type_
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.AnnouncementAction"
