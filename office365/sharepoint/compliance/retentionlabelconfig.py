from typing import Optional

from office365.runtime.client_value import ClientValue


class SPRetentionLabelConfig(ClientValue):
    def __init__(self, id_: Optional[str] = None, name: Optional[str] = None):
        self.Id = id_
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPRetentionLabelConfig"
