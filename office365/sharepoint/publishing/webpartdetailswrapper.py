from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WebPartDetailsWrapper(ClientValue):
    InstanceId: Optional[str] = None
    IsInternal: Optional[bool] = None
    ManifestId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.WebPartDetailsWrapper"
