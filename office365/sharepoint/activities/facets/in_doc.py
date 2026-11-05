from __future__ import annotations

from office365.runtime.client_value import ClientValue


class InDocFacet(ClientValue):
    contentId: str | None = None
    navigationId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.InDocFacet"
