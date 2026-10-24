from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.body_type import BodyType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class ItemBody(ClientValue):
    """Represents properties of the body of an item, such as a message, event or group post."""

    #: The service re-wraps every body it accepts in its own markup: the text is the content.
    content: str | None = field(default=None, metadata=odata("content", compare=Compare(format="text")))
    contentType: BodyType = field(default=BodyType.text, metadata=odata("contentType", compare=Compare(ignore=True)))

    @staticmethod
    def text(content: str) -> "ItemBody":
        return ItemBody(content)

    @staticmethod
    def html(content: str) -> "ItemBody":
        return ItemBody(content, BodyType.html)

    def __repr__(self):
        return self.content or ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ItemBody"
