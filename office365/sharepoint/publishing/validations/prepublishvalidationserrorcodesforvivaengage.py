from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.destinationv2 import VivaEngageDestinationV2 as _VivaEngageDestinationV2


@dataclass
class PrePublishValidationsErrorCodesForVivaEngage(ClientValue):
    DestinationName: Optional[str] = None
    DestinationType: Optional[int] = None
    ErrorCodes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    NumberOfImageAttachments: Optional[int] = None
    VivaEngageDestinationV2: _VivaEngageDestinationV2 = field(default_factory=lambda: _VivaEngageDestinationV2())

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForVivaEngage"
