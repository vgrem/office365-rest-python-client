from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SharePageByEmailData(ClientValue):
    BccEmails: StringCollection = field(default_factory=StringCollection)
    CcEmails: StringCollection = field(default_factory=StringCollection)
    EmailSize: Optional[str] = None
    Message: Optional[str] = None
    PageContent: Optional[str] = None
    PageItemId: Optional[int] = None
    RecipientEmails: StringCollection = field(default_factory=StringCollection)
    ScenarioTag: Optional[str] = None
    Subject: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePageByEmailData"
