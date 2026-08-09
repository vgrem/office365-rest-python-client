from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SettingTemplateValue(ClientValue):
    defaultValue: str | None = None
    description: str | None = None
    name: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SettingTemplateValue"
