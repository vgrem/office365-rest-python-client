from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class PrePublishValidationsErrorCodesForSharePointSite(ClientValue):
    ErrorCodes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    SiteId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForSharePointSite"
