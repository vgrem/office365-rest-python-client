from __future__ import annotations

from office365.intune.devices.management.mobileapps.win32.lob_app_rule import Win32LobAppRule
from office365.intune.devices.management.mobileapps.win32.ruleoperator import (
    Win32LobAppRuleOperator,
)


class Win32LobAppProductCodeRule(Win32LobAppRule):
    productCode: str | None = None
    productVersion: str | None = None
    productVersionOperator: Win32LobAppRuleOperator = Win32LobAppRuleOperator.notConfigured

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobAppProductCodeRule"
