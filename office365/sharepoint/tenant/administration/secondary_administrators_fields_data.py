from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SecondaryAdministratorsFieldsData(ClientValue):
    siteId: str | None = None
    secondaryAdministratorEmails: StringCollection | None = None
    secondaryAdministratorLoginNames: StringCollection | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData"
