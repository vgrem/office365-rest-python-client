from __future__ import annotations

from dataclasses import field

from office365.backuprestore.restorepoints.search_result import RestorePointSearchResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class RestorePointSearchResponse(ClientValue):
    noResultProtectionUnitIds: StringCollection = field(default_factory=StringCollection)
    searchResponseId: str | None = None
    searchResults: ClientValueCollection[RestorePointSearchResult] = field(
        default_factory=lambda: ClientValueCollection(RestorePointSearchResult)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestorePointSearchResponse"
