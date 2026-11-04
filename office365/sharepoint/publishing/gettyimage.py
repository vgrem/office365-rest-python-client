from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class GettyImage(ClientValue):
    ImageId: Optional[str] = None
    ImageUrl: Optional[str] = None
    InsertionISOTimestamp: Optional[str] = None
    PrimaryId: Optional[str] = None
    SecondaryId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.GettyImage"
