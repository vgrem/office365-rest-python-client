from typing import Optional

from office365.runtime.client_value import ClientValue


class RevisionInfo(ClientValue):
    def __init__(self, id_: Optional[str] = None):
        self.id = id_

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.RevisionInfo"
