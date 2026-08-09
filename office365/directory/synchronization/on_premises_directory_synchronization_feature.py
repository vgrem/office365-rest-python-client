from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class OnPremisesDirectorySynchronizationFeature(ClientValue):
    allowOnPremUpdateOfOnPremisesObjectIdentifierEnabled: bool | None = None
    blockCloudObjectTakeoverThroughHardMatchEnabled: bool | None = None
    blockSoftMatchEnabled: bool | None = None
    bypassDirSyncOverridesEnabled: bool | None = None
    cloudPasswordPolicyForPasswordSyncedUsersEnabled: bool | None = None
    concurrentCredentialUpdateEnabled: bool | None = None
    concurrentOrgIdProvisioningEnabled: bool | None = None
    deviceWritebackEnabled: bool | None = None
    directoryExtensionsEnabled: bool | None = None
    fopeConflictResolutionEnabled: bool | None = None
    groupWriteBackEnabled: bool | None = None
    passwordSyncEnabled: bool | None = None
    passwordWritebackEnabled: bool | None = None
    quarantineUponProxyAddressesConflictEnabled: bool | None = None
    quarantineUponUpnConflictEnabled: bool | None = None
    softMatchOnUpnEnabled: bool | None = None
    synchronizeUpnForManagedUsersEnabled: bool | None = None
    unifiedGroupWritebackEnabled: bool | None = None
    userForcePasswordChangeOnLogonEnabled: bool | None = None
    userWritebackEnabled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesDirectorySynchronizationFeature"
