from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class PrePublishValidationsErrorCodesForTeams(ClientValue):
    AudienceId: Optional[str] = None
    ErrorCodes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    NumberOfImagesInPayload: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForTeams"
