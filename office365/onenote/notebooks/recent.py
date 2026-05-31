from __future__ import annotations

from dataclasses import dataclass, field

from office365.onenote.notebooks.recent_links import RecentNotebookLinks
from office365.runtime.client_value import ClientValue


@dataclass
class RecentNotebook(ClientValue):
    """A recently accessed OneNote notebook. A recentNotebook is similar to a notebook but has fewer properties.

    :param str display_name: The name of the notebook.
    :param RecentNotebookLinks links: Links for opening the notebook.
        The oneNoteClientURL link opens the notebook in the OneNote client, if it's installed.
        The oneNoteWebURL link opens the notebook in OneNote on the web.
    """

    displayName: str | None = None
    lastAccessedTime: str | None = None
    links: RecentNotebookLinks = field(default_factory=RecentNotebookLinks)
    sourceService: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecentNotebook"
