from __future__ import annotations

from office365.directory.policies.cloudappsecuritysessioncontroltype import CloudAppSecuritySessionControlType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudAppSecuritySessionControl(ClientValue):
    cloudAppSecurityType: CloudAppSecuritySessionControlType = CloudAppSecuritySessionControlType.mcasConfigured

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudAppSecuritySessionControl"
