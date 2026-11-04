from __future__ import annotations

from office365.intune.devices.management.mobileapps.win32.ruleoperator import (
    Win32LobAppRuleOperator,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Win32LobAppProductCodeRule(ClientValue):
    productCode: str | None = None
    productVersion: str | None = None
    productVersionOperator: Win32LobAppRuleOperator = Win32LobAppRuleOperator.notConfigured

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobAppProductCodeRule"
