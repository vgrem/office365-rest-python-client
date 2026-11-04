from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SocialDataItem(ClientValue):
    AccountName: Optional[str] = None
    ItemType: Optional[int] = None
    TagGuid: Optional[str] = None
    Text: Optional[str] = None
    Uri: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialDataItem"
