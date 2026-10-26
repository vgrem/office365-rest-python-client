from __future__ import annotations

from dataclasses import dataclass, field

from office365.backuprestore.backup_count_statistics import BackupCountStatistics
from office365.runtime.client_value import ClientValue


@dataclass
class BackupPolicyReport(ClientValue):
    backupPolicyId: str | None = None
    countStatistics: BackupCountStatistics = field(default_factory=BackupCountStatistics)
    displayName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BackupPolicyReport"
