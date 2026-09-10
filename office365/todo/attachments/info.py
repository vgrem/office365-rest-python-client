from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.todo.attachments.type import AttachmentType


@dataclass
class AttachmentInfo(ClientValue):
    """Represents the attributes of an attachment to be uploaded to a todoTask."""

    attachmentType: Optional[AttachmentType] = None
    contentType: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.attachmentInfo"
