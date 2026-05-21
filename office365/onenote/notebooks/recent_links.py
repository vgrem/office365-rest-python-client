from dataclasses import dataclass, field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue


@dataclass
class RecentNotebookLinks(ClientValue):
    """
    Links for opening a OneNote notebook. This resource type exists as a property on a recentNotebook resource.
    """

    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)
