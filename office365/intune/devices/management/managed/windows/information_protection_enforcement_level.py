from __future__ import annotations

from enum import Enum


class WindowsInformationProtectionEnforcementLevel(Enum):
    noProtection = "0"
    encryptAndAuditOnly = "1"
    encryptAuditAndPrompt = "2"
    encryptAuditAndBlock = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionEnforcementLevel"
