from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MigrationProperty(ClientValue):
    key: Optional[str] = None
    updatedTimeUtc: Optional[datetime] = None
    value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationProperty"
