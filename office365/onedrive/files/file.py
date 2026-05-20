from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class File(ClientValue):
    """
    The File resource groups file-related data items into a single structure.

    If a DriveItem has a non-null file facet, the item represents a file.
    In addition to other properties, files have a content relationship which contains the byte stream of the file.
    """

    hashes: str | None = None
    mimeType: str | None = None
    processingMetadata: str | None = field(default=None, init=False)
