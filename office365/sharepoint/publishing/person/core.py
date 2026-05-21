from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PersonCore(ClientValue):
    AadObjectId: Optional[str] = None
    DisplayName: Optional[str] = None
    UserName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonCore"
