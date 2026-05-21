from dataclasses import dataclass
from typing import List, Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SharePagePreviewByEmailFieldsData(ClientValue):
    message: Optional[str] = None
    recipientEmails: Optional[List[str]] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePagePreviewByEmailFieldsData"
