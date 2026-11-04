from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.datasecurity.classification_inner_error import ClassificationInnerError


@value
class ClassifcationErrorBase(ClientValue):
    code: str | None = None
    innerError: ClassificationInnerError = field(default_factory=ClassificationInnerError)
    message: str | None = None
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ClassifcationErrorBase"
