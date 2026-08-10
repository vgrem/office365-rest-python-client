from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.backuprestore.backupserviceconsumer import BackupServiceConsumer
from office365.backuprestore.backupservicestatus import BackupServiceStatus
from office365.backuprestore.disablereason import DisableReason
from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


class ServiceStatus(ClientValue):
    stopped = "1"
    starting = "2"
    running = "3"
    disabled = "4"
    onboarding = "5"
    unknown = "6"
    unknownFutureValue = "7"
    "Represents the tenant-level service status of the backup service."
    backupServiceConsumer: BackupServiceConsumer = BackupServiceConsumer.unknown
    disableReason: DisableReason = DisableReason.none
    gracePeriodDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    lastModifiedBy: IdentitySet = field(default_factory=IdentitySet)
    lastModifiedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    restoreAllowedTillDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    status: BackupServiceStatus = BackupServiceStatus.disabled

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ServiceStatus"
