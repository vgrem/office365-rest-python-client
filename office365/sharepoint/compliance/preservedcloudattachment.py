from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PreservedCloudAttachment(ClientValue):
    CompositeDocumentId: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ComplianceFoundation.Models.PreservedCloudAttachment"
