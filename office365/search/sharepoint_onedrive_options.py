from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharePointOneDriveOptions(ClientValue):
    """Provides the search content options when a search is performed using application permissions

    Fields:
        searchContent:
    """

    searchContent: str | None = None
