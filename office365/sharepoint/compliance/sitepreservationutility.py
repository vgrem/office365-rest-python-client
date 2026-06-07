from office365.sharepoint.entity import Entity


class SPSitePreservationUtility(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.CompliancePolicy.SPSitePreservationUtility"
