from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class ShortcutInformation(ClientValue):
    def __init__(
        self,
        added_by_id: Optional[int] = None,
        id_: Optional[str] = None,
        name: Optional[str] = None,
        scenario: Optional[int] = None,
        time_created: Optional[datetime] = None,
        time_last_modified: Optional[datetime] = None,
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
