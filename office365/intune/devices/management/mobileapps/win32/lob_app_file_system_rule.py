from __future__ import annotations

from office365.intune.devices.management.mobileapps.win32.filesystemoperationtype import (
    Win32LobAppFileSystemOperationType,
)
from office365.intune.devices.management.mobileapps.win32.lob_app_rule import Win32LobAppRule
from office365.intune.devices.management.mobileapps.win32.ruleoperator import (
    Win32LobAppRuleOperator,
)


class Win32LobAppFileSystemRule(Win32LobAppRule):
    check32BitOn64System: bool | None = None
    comparisonValue: str | None = None
    fileOrFolderName: str | None = None
    operationType: Win32LobAppFileSystemOperationType = Win32LobAppFileSystemOperationType.notConfigured
    operator: Win32LobAppRuleOperator = Win32LobAppRuleOperator.notConfigured
    path: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobAppFileSystemRule"
