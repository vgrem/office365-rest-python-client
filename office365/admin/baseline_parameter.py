from __future__ import annotations

from office365.admin.baseline_parameter_type import BaselineParameterType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class BaselineParameter(ClientValue):
    description: str | None = None
    displayName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BaselineParameter"

    parameterType: BaselineParameterType = BaselineParameterType.string
