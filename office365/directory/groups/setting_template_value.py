from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SettingTemplateValue(ClientValue):
    defaultValue: str | None = None
    description: str | None = None
    name: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SettingTemplateValue"
