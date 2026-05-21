from dataclasses import dataclass, field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


@dataclass
class PageLinks(ClientValue):
    """Links for opening a OneNote page.

    :param ExternalLink onenote_client_url: Opens the page in the OneNote native client if it's installed.
    :param ExternalLink onenote_web_url: Opens the page in OneNote on the web.
    """

    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)
