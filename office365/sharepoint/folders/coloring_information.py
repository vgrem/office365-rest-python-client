from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.folders.colors import FolderColors


class FolderColoringInformation(ClientValue):
    """"""

    def __init__(self, color_hex: Optional[FolderColors] = None, color_tag: Optional[str] = None, emoji: Optional[str] = None):
        """
        :param FolderColors color_hex:
        :param str color_tag:
        :param str emoji:
        """
        self.ColorHex = color_hex
        self.ColorTag = color_tag
        self.Emoji = emoji

    @property
    def entity_type_name(self):
        return "SP.FolderColoringInformation"
