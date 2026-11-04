from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MigrationProperty(ClientValue):
    key: Optional[str] = None
    updatedTimeUtc: Optional[datetime] = None
    value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationProperty"
