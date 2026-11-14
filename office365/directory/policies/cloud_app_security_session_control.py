from __future__ import annotations

from office365.directory.identities.conditional_access_session_control import ConditionalAccessSessionControl
from office365.directory.policies.cloudappsecuritysessioncontroltype import CloudAppSecuritySessionControlType


class CloudAppSecuritySessionControl(ConditionalAccessSessionControl):
    cloudAppSecurityType: CloudAppSecuritySessionControlType = CloudAppSecuritySessionControlType.mcasConfigured

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudAppSecuritySessionControl"
