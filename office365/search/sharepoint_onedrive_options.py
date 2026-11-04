from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.search.content import SearchContent


@value
class SharePointOneDriveOptions(ClientValue):
    """Provides the search content options when a search is performed using application permissions

    Fields:
        searchContent:
    """

    searchContent: str | None = None

    includeContent: SearchContent = SearchContent.sharedContent

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointOneDriveOptions"
