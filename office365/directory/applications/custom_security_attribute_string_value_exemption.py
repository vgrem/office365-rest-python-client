from __future__ import annotations

from office365.directory.applications.custom_security_attribute_exemption import CustomSecurityAttributeExemption


class CustomSecurityAttributeStringValueExemption(CustomSecurityAttributeExemption):
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomSecurityAttributeStringValueExemption"
