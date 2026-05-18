from __future__ import annotations

from dataclasses import dataclass

from office365.outlook.mail.body_type import BodyType
from office365.runtime.client_value import ClientValue


@dataclass
class ItemBody(ClientValue):
    """Represents properties of the body of an item, such as a message, event or group post."""

    content: str | None = None
    contentType: BodyType = BodyType.text

    @staticmethod
    def text(content: str) -> "ItemBody":
        return ItemBody(content)

    @staticmethod
    def html(content: str) -> "ItemBody":
        return ItemBody(content, BodyType.html)

    def __repr__(self):
        return self.content or ""
