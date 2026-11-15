from __future__ import annotations

from enum import Enum


class MailFolderOperationStatus(Enum):
    notStarted = "0"
    running = "1"
    succeeded = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailFolderOperationStatus"
