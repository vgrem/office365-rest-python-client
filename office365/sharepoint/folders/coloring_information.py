from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.sharepoint.folders.colors import FolderColors


class FolderColoringInformation(ClientValue):
    """"""

    ColorHex: FolderColors | None = None
    ColorTag: str | None = None
    Emoji: str | None = None

    @property
    def entity_type_name(self):
        return "SP.FolderColoringInformation"
