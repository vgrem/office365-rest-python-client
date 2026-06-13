from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BulkRetireTaskParameters(ClientValue):
    ForceRetire: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BulkRetireTaskParameters"
