from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.management.virtualendpoint.cloudpcs.userrolescopetaginfo import CloudPcUserRoleScopeTagInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class CloudPcAuditActor(ClientValue):
    applicationDisplayName: str | None = None
    applicationId: str | None = None
    ipAddress: str | None = None
    remoteTenantId: str | None = None
    remoteUserId: str | None = None
    servicePrincipalName: str | None = None
    userId: str | None = None
    userPermissions: StringCollection = field(default_factory=StringCollection)
    userPrincipalName: str | None = None
    userRoleScopeTags: ClientValueCollection[CloudPcUserRoleScopeTagInfo] = field(
        default_factory=lambda: ClientValueCollection(CloudPcUserRoleScopeTagInfo)
    )

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditActor"
