from datetime import datetime

from office365.runtime.client_value import ClientValue


class ShortcutInformation(ClientValue):

    def __init__(
        self,
        added_by_id: int = None,
        id_: str = None,
        name: str = None,
        scenario: int = None,
        time_created: datetime = None,
        time_last_modified: datetime = None,
    ):
        self.AddedById = added_by_id
        self.Id = id_
        self.Name = name
        self.Scenario = scenario
        self.TimeCreated = time_created
        self.TimeLastModified = time_last_modified

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Deployment.ShortcutInformation"
