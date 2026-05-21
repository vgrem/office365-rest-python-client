from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class WikiPageCreationInformation(ClientValue):

    """
    Specifies wiki page creation information

    :param str server_relative_url: The server-relative URL of the wiki page to be created.
    :param str content: The HTML content of the wiki page.
    """

    ServerRelativeUrl: Optional[str] = None
    WikiHtmlContent: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.WikiPageCreationInformation"