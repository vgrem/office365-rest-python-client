from __future__ import annotations

from office365.intune.devices.configurations.sharedpc.accountdeletionpolicytype import (
    SharedPCAccountDeletionPolicyType,
)
from office365.runtime.client_value import ClientValue


class SharedPCAccountManagerPolicy(ClientValue):
    accountDeletionPolicy: SharedPCAccountDeletionPolicyType = SharedPCAccountDeletionPolicyType.immediate
    cacheAccountsAboveDiskFreePercentage: int | None = None
    inactiveThresholdDays: int | None = None
    removeAccountsBelowDiskFreePercentage: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharedPCAccountManagerPolicy"
