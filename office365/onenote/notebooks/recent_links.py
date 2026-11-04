from dataclasses import field

from office365.onenote.pages.external_link import ExternalLink
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RecentNotebookLinks(ClientValue):
    """
    Links for opening a OneNote notebook. This resource type exists as a property on a recentNotebook resource.
    """

    oneNoteClientUrl: ExternalLink = field(default_factory=ExternalLink)
    oneNoteWebUrl: ExternalLink = field(default_factory=ExternalLink)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecentNotebookLinks"
