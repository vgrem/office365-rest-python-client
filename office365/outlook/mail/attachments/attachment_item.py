from __future__ import annotations

import os
from dataclasses import dataclass

from office365.outlook.mail.attachments.type import AttachmentType
from office365.runtime.client_value import ClientValue


@dataclass
class AttachmentItem(ClientValue):
    """Represents attributes of an item to be attached."""

    attachmentType: AttachmentType | None = None
    name: str | None = None
    size: int | None = None

    @staticmethod
    def create_file(path: str) -> "AttachmentItem":
        file_name = os.path.basename(path)
        file_size = os.stat(path).st_size
        from office365.outlook.mail.attachments.type import AttachmentType

        return AttachmentItem(attachmentType=AttachmentType.file, name=file_name, size=file_size)
