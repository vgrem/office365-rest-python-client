from office365.runtime.client_value import ClientValue


class GeoMoveTenantPropertyCompatibilityCheck(ClientValue):

    def __init__(
        self,
        geo_move_tenant_property_check_result: int = None,
        property_name: str = None,
    ):
        self.GeoMoveTenantPropertyCheckResult = geo_move_tenant_property_check_result
        self.PropertyName = property_name
