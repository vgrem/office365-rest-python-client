from typing import Optional

from office365.runtime.client_value import ClientValue


class SPRetentionLabelConfig(ClientValue):
    Id: Optional[str] = None
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPRetentionLabelConfig"
