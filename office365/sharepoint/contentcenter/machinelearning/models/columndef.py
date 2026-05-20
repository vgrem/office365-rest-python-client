from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ColumnDef(ClientValue):
    CustomFormatter: Optional[str] = None
    Id: Optional[str] = None
    Name: Optional[str] = None
    Type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.ColumnDef"
