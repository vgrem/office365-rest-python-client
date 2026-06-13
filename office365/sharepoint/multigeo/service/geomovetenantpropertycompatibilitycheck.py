from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GeoMoveTenantPropertyCompatibilityCheck(ClientValue):
    GeoMoveTenantPropertyCheckResult: Optional[int] = None
    PropertyName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoMoveTenantPropertyCompatibilityCheck"
