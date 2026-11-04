from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.custom_security_attribute_comparison_operator import (
    CustomSecurityAttributeComparisonOperator,
)


@value
class CustomSecurityAttributeExemption(ClientValue):
    id: str | None = None
    operator: CustomSecurityAttributeComparisonOperator = CustomSecurityAttributeComparisonOperator.equals

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomSecurityAttributeExemption"
