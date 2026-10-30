from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.applications.templateapplicationlevel import TemplateApplicationLevel
from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.crosstenant.b2_b_setting import (
        CrossTenantAccessPolicyB2BSetting,
    )
    from office365.directory.policies.crosstenant.inbound_trust import (
        CrossTenantAccessPolicyInboundTrust,
    )
    from office365.directory.policies.inbound_outbound_policy_configuration import (
        InboundOutboundPolicyConfiguration,
    )


class MultiTenantOrganizationPartnerConfigurationTemplate(Entity):
    @odata(name="automaticUserConsentSettings")
    @property
    def automatic_user_consent_settings(self) -> InboundOutboundPolicyConfiguration:
        """Gets the automaticUserConsentSettings property"""
        from office365.directory.policies.inbound_outbound_policy_configuration import (
            InboundOutboundPolicyConfiguration,
        )

        return self.properties.get("automaticUserConsentSettings", InboundOutboundPolicyConfiguration())

    @odata(name="b2bCollaborationInbound")
    @property
    def b2b_collaboration_inbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bCollaborationInbound property"""
        from office365.directory.policies.crosstenant.b2_b_setting import (
            CrossTenantAccessPolicyB2BSetting,
        )

        return self.properties.get("b2bCollaborationInbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bCollaborationOutbound")
    @property
    def b2b_collaboration_outbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bCollaborationOutbound property"""
        from office365.directory.policies.crosstenant.b2_b_setting import (
            CrossTenantAccessPolicyB2BSetting,
        )

        return self.properties.get("b2bCollaborationOutbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bDirectConnectInbound")
    @property
    def b2b_direct_connect_inbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bDirectConnectInbound property"""
        from office365.directory.policies.crosstenant.b2_b_setting import (
            CrossTenantAccessPolicyB2BSetting,
        )

        return self.properties.get("b2bDirectConnectInbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="b2bDirectConnectOutbound")
    @property
    def b2b_direct_connect_outbound(self) -> CrossTenantAccessPolicyB2BSetting:
        """Gets the b2bDirectConnectOutbound property"""
        from office365.directory.policies.crosstenant.b2_b_setting import (
            CrossTenantAccessPolicyB2BSetting,
        )

        return self.properties.get("b2bDirectConnectOutbound", CrossTenantAccessPolicyB2BSetting())

    @odata(name="inboundTrust")
    @property
    def inbound_trust(self) -> CrossTenantAccessPolicyInboundTrust:
        """Gets the inboundTrust property"""
        from office365.directory.policies.crosstenant.inbound_trust import (
            CrossTenantAccessPolicyInboundTrust,
        )

        return self.properties.get("inboundTrust", CrossTenantAccessPolicyInboundTrust())

    @odata(name="templateApplicationLevel")
    @property
    def template_application_level(self) -> TemplateApplicationLevel:
        """Gets the templateApplicationLevel property"""
        return self.properties.get("templateApplicationLevel", TemplateApplicationLevel.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantOrganizationPartnerConfigurationTemplate"
