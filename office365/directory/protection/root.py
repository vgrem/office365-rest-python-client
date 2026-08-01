from office365.directory.protection.risk_detection import RiskDetection
from office365.directory.protection.riskyusers.collection import RiskyUserCollection
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class IdentityProtectionRoot(Entity):
    """Container for the navigation properties for Microsoft Graph identity protection resources."""

    @odata(name="riskDetections")
    @property
    def risk_detections(self) -> EntityCollection[RiskDetection]:
        """Risk detection in Azure AD Identity Protection and the associated information about the detection."""
        return self.properties.get(
            "riskDetections",
            EntityCollection(self.context, RiskDetection, ResourcePath("riskDetections", self.resource_path)),
        )

    @odata(name="riskyUsers")
    @property
    def risky_users(self) -> RiskyUserCollection:
        """Get the teams in Microsoft Teams that the user is a direct member of."""
        return self.properties.get(
            "riskyUsers", RiskyUserCollection(self.context, ResourcePath("riskyUsers", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdentityProtectionRoot"
