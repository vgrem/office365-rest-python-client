from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class PrePublishValidationsErrorCodesForEmail(ClientValue):
    EmailAddress: Optional[str] = None
    ErrorCodes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForEmail"
