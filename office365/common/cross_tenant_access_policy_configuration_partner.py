from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.policies.crosstenant.app_service_connect_setting import (  # noqa: E501
    CrossTenantAccessPolicyAppServiceConnectSetting,
)
from office365.directory.policies.crosstenant.b2_b_setting import CrossTenantAccessPolicyB2BSetting
from office365.directory.policies.crosstenant.inbound_trust import CrossTenantAccessPolicyInboundTrust
from office365.directory.policies.crosstenant.m365_collaboration_inbound_setting import (  # noqa: E501
    CrossTenantAccessPolicyM365CollaborationInboundSetting,
)
from office365.directory.policies.crosstenant.m365_collaboration_outbound_setting import (  # noqa: E501
    CrossTenantAccessPolicyM365CollaborationOutboundSetting,
)
from office365.directory.policies.crosstenant.tenant_restrictions import CrossTenantAccessPolicyTenantRestrictions
from office365.directory.policies.inbound_outbound_policy_configuration import InboundOutboundPolicyConfiguration
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import key, odata

if TYPE_CHECKING:
    from office365.common.cross_tenant_identity_sync_policy_partner import (
        CrossTenantIdentitySyncPolicyPartner,
    )
    from office365.directory.service_provider_constraints import (
        ServiceProviderConstraints,
    )
    from office365.intune.devices.management.m365_capability_base import M365CapabilityBase


@key("tenantId")
class CrossTenantAccessPolicyConfigurationPartner(Entity):
    @odata(name="appServiceConnectInbound")
    @property
    def app_service_connect_inbound(self) -> CrossTenantAccessPolicyAppServiceConnectSetting:
        """Gets the appServiceConnectInbound property"""
        return self.properties.get("appServiceConnectInbound", CrossTenantAccessPolicyAppServiceConnectSetting())

    @odata(name="automaticUserConsentSettings")
    @property
    def automatic_user_consent_settings(self) -> InboundOutboundPolicyConfiguration:
        """Gets the automaticUserConsentSettings property"""
        return self.properties.get("automaticUserConsentSettings", InboundOutboundPolicyConfiguration())

    @odata(name="b2bCollaborationInbound")
    @property
    def b2b_collaboration_inbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bCollaborationInbound property"""
        return self.properties.get("b2bCollaborationInbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bCollaborationOutbound")
    @property
    def b2b_collaboration_outbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bCollaborationOutbound property"""
        return self.properties.get("b2bCollaborationOutbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bDirectConnectInbound")
    @property
    def b2b_direct_connect_inbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bDirectConnectInbound property"""
        return self.properties.get("b2bDirectConnectInbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bDirectConnectOutbound")
    @property
    def b2b_direct_connect_outbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bDirectConnectOutbound property"""
        return self.properties.get("b2bDirectConnectOutbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="inboundTrust")
    @property
    def inbound_trust(self) -> CrossTenantAccessPolicyInboundTrust:
        """Gets the inboundTrust property"""
        return self.properties.get("inboundTrust", CrossTenantAccessPolicyInboundTrust())

    @odata(name="isInMultiTenantOrganization")
    @property
    def is_in_multi_tenant_organization(self) -> Optional[bool]:
        """Gets the isInMultiTenantOrganization property"""
        return self.properties.get("isInMultiTenantOrganization", None)

    @odata(name="isServiceProvider")
    @property
    def is_service_provider(self) -> Optional[bool]:
        """Gets the isServiceProvider property"""
        return self.properties.get("isServiceProvider", None)

    @odata(name="m365CollaborationInbound")
    @property
    def m365_collaboration_inbound(self) -> CrossTenantAccessPolicyM365CollaborationInboundSetting:
        """Gets the m365CollaborationInbound property"""
        return self.properties.get("m365CollaborationInbound", CrossTenantAccessPolicyM365CollaborationInboundSetting())

    @odata(name="m365CollaborationOutbound")
    @property
    def m365_collaboration_outbound(self) -> CrossTenantAccessPolicyM365CollaborationOutboundSetting:
        """Gets the m365CollaborationOutbound property"""
        return self.properties.get(
            "m365CollaborationOutbound", CrossTenantAccessPolicyM365CollaborationOutboundSetting()
        )

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="tenantRestrictions")
    @property
    def tenant_restrictions(self) -> CrossTenantAccessPolicyTenantRestrictions:
        """Gets the tenantRestrictions property"""
        return self.properties.get("tenantRestrictions", CrossTenantAccessPolicyTenantRestrictions())

    @odata(name="identitySynchronization", navigation=True)
    @property
    def identity_synchronization(self) -> CrossTenantIdentitySyncPolicyPartner:
        """Gets the identitySynchronization property"""
        from office365.common.cross_tenant_identity_sync_policy_partner import (
            CrossTenantIdentitySyncPolicyPartner,
        )

        return self.properties.get(
            "identitySynchronization",
            CrossTenantIdentitySyncPolicyPartner(
                self.context, ResourcePath("identitySynchronization", self.resource_path)
            ),
        )

    @odata(name="serviceProviderConstraints", navigation=True)
    @property
    def service_provider_constraints(self) -> ServiceProviderConstraints:
        """Gets the serviceProviderConstraints property"""
        from office365.directory.service_provider_constraints import (
            ServiceProviderConstraints,
        )

        return self.properties.get(
            "serviceProviderConstraints",
            ServiceProviderConstraints(self.context, ResourcePath("serviceProviderConstraints", self.resource_path)),
        )

    @odata(name="m365Capabilities", navigation=True)
    @property
    def m365_capabilities(self) -> EntityCollection[M365CapabilityBase]:
        """Gets the m365Capabilities property"""
        from office365.intune.devices.management.m365_capability_base import M365CapabilityBase

        return self.properties.get(
            "m365Capabilities",
            EntityCollection[M365CapabilityBase](
                self.context, M365CapabilityBase, ResourcePath("m365Capabilities", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantAccessPolicyConfigurationPartner"
