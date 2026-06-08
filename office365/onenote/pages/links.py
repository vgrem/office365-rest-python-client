from dataclasses import dataclass, field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


@dataclass
class PageLinks(ClientValue):
    """Links for opening a OneNote page.

    Args:
        onenote_client_url (ExternalLink): Opens the page in the OneNote native client if it's installed.
        onenote_web_url (ExternalLink): Opens the page in OneNote on the web.
    """

    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PageLinks"
