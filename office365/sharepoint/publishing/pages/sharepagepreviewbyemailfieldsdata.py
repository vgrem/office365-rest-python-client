from typing import List, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SharePagePreviewByEmailFieldsData(ClientValue):
    message: Optional[str] = None
    recipientEmails: Optional[List[str]] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePagePreviewByEmailFieldsData"
