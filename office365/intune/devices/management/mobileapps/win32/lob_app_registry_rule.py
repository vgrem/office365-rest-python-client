from __future__ import annotations

from office365.intune.devices.management.mobileapps.win32.lob_app_rule import Win32LobAppRule
from office365.intune.devices.management.mobileapps.win32.registryruleoperationtype import (
    Win32LobAppRegistryRuleOperationType,
)
from office365.intune.devices.management.mobileapps.win32.ruleoperator import (
    Win32LobAppRuleOperator,
)


class Win32LobAppRegistryRule(Win32LobAppRule):
    check32BitOn64System: bool | None = None
    comparisonValue: str | None = None
    keyPath: str | None = None
    operationType: Win32LobAppRegistryRuleOperationType = Win32LobAppRegistryRuleOperationType.notConfigured
    operator: Win32LobAppRuleOperator = Win32LobAppRuleOperator.notConfigured
    valueName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobAppRegistryRule"
