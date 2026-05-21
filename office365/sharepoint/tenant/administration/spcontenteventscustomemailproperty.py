from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SPContentEventsCustomEmailProperty(ClientValue):
    Category: int | None = None
    EmailAddresses: StringCollection = field(default_factory=lambda: StringCollection())

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPContentEventsCustomEmailProperty"
