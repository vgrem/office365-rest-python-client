from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPDependentModel(ClientValue):
    LastRefereshedTimeUtc: Optional[datetime] = None
    ModelId: Optional[str] = None
    ModelType: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPDependentModel"
