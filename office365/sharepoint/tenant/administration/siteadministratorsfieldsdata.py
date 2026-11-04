from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class SiteAdministratorsFieldsData(ClientValue):
    siteAdministrators: StringCollection = field(default_factory=StringCollection)
    siteId: UUID | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsFieldsData"
