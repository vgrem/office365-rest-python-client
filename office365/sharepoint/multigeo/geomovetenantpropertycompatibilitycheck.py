from office365.runtime.client_value import ClientValue
from typing import Optional


class GeoMoveTenantPropertyCompatibilityCheck(ClientValue):
    def __init__(
        self,
        geo_move_tenant_property_check_result: Optional[int] = None,
        property_name: Optional[str] = None,
    ):
        self.GeoMoveTenantPropertyCheckResult = geo_move_tenant_property_check_result
        self.PropertyName = property_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoMoveTenantPropertyCompatibilityCheck"
