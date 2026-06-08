from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WikiPageCreationInformation(ClientValue):
    """Specifies wiki page creation information

    Args:
        server_relative_url (str): The server-relative URL of the wiki page to be created.
        content (str): The HTML content of the wiki page.
    """

    ServerRelativeUrl: Optional[str] = None
    WikiHtmlContent: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.WikiPageCreationInformation"
