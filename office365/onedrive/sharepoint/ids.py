from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SharePointIds(ClientValue):
    """The SharePointIds resource groups the various identifiers for an item stored in a SharePoint site or OneDrive
    for Business into a single structure."""

    listId: str | None = None
    listItemId: str | None = None
    listItemUniqueId: str | None = None
    siteId: str | None = None
    siteUrl: str | None = None
    tenantId: str | None = None
    webId: str | None = None
