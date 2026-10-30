from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.information import ComplianceInformation
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.security.securescores.control_state_update import SecureScoreControlStateUpdate
from office365.security.security_vendor_information import SecurityVendorInformation


class SecureScoreControlProfile(Entity):
    """Represents a tenant's secure score per control data. By default, it returns all controls
    for a tenant and can explicitly pull individual controls."""

    @odata(name="actionType")
    @property
    def action_type(self) -> Optional[str]:
        """Control action type (Config, Review, Behavior)."""
        return self.properties.get("actionType", None)

    @odata(name="actionUrl")
    @property
    def action_url(self) -> Optional[str]:
        """URL to where the control can be actioned."""
        return self.properties.get("actionUrl", None)

    @odata(name="azureTenantId")
    @property
    def azure_tenant_id(self) -> Optional[str]:
        """GUID string for tenant ID."""
        return self.properties.get("azureTenantId", None)

    @odata(name="complianceInformation")
    @property
    def compliance_information(self) -> ClientValueCollection[ComplianceInformation]:
        """Gets the complianceInformation property"""
        return self.properties.get(
            "complianceInformation", ClientValueCollection[ComplianceInformation](ComplianceInformation)
        )

    @odata(name="controlCategory")
    @property
    def control_category(self) -> Optional[str]:
        """Gets the controlCategory property"""
        return self.properties.get("controlCategory", None)

    @odata(name="controlStateUpdates")
    @property
    def control_state_updates(self) -> ClientValueCollection[SecureScoreControlStateUpdate]:
        """Gets the controlStateUpdates property"""
        return self.properties.get(
            "controlStateUpdates", ClientValueCollection[SecureScoreControlStateUpdate](SecureScoreControlStateUpdate)
        )

    @odata(name="deprecated")
    @property
    def deprecated(self) -> Optional[bool]:
        """Gets the deprecated property"""
        return self.properties.get("deprecated", None)

    @odata(name="implementationCost")
    @property
    def implementation_cost(self) -> Optional[str]:
        """Gets the implementationCost property"""
        return self.properties.get("implementationCost", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="maxScore")
    @property
    def max_score(self) -> Optional[float]:
        """Gets the maxScore property"""
        return self.properties.get("maxScore", None)

    @odata(name="rank")
    @property
    def rank(self) -> Optional[int]:
        """Gets the rank property"""
        return self.properties.get("rank", None)

    @odata(name="remediation")
    @property
    def remediation(self) -> Optional[str]:
        """Gets the remediation property"""
        return self.properties.get("remediation", None)

    @odata(name="remediationImpact")
    @property
    def remediation_impact(self) -> Optional[str]:
        """Gets the remediationImpact property"""
        return self.properties.get("remediationImpact", None)

    @odata(name="service")
    @property
    def service(self) -> Optional[str]:
        """Gets the service property"""
        return self.properties.get("service", None)

    @odata(name="threats")
    @property
    def threats(self) -> StringCollection:
        """Gets the threats property"""
        return self.properties.get("threats", StringCollection())

    @odata(name="tier")
    @property
    def tier(self) -> Optional[str]:
        """Gets the tier property"""
        return self.properties.get("tier", None)

    @odata(name="title")
    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @odata(name="userImpact")
    @property
    def user_impact(self) -> Optional[str]:
        """Gets the userImpact property"""
        return self.properties.get("userImpact", None)

    @odata(name="vendorInformation")
    @property
    def vendor_information(self) -> SecurityVendorInformation:
        """Gets the vendorInformation property"""
        return self.properties.get("vendorInformation", SecurityVendorInformation())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SecureScoreControlProfile"
