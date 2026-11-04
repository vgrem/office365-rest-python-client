from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPSensitivityLabelConfig(ClientValue):
    Id: Optional[str] = None
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPSensitivityLabelConfig"
