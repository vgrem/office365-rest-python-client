from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CreatableItemInfo(ClientValue):
    """Information on a creatable item: what the item is and where to go to create it. Alternatively, the information
    provided here can be used to call CreateDocument (section 3.2.5.79.2.2.9) or
    CreateDocumentAndGetEditLink (section 3.2.5.79.2.1.13)

    Fields:
        DocumentTemplate (int):
        FileExtension (str):
        ItemType (str):
    """

    DocumentTemplate: Optional[int] = None
    FileExtension: Optional[str] = None
    ItemType: Optional[str] = None
