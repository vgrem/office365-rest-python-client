from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AttachmentCreationInformation(ClientValue):
    """Represents properties that can be set when creating a file by using the AttachmentFiles.Add method.

    Args:
        filename (str): Specifies the file name of the list item attachment.
        content (str or bytes): The contents of the file as a stream.
    """

    filename: Optional[str] = None
    content: Optional[bytes] = None
    FileName: Optional[str] = None
