from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.datasecurity.classification_inner_error import ClassificationInnerError
from office365.runtime.client_value import ClientValue


@dataclass
class ClassificationErrorBase(ClientValue):
    code: str | None = None
    innerError: ClassificationInnerError = field(default_factory=ClassificationInnerError)
    message: str | None = None
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ClassificationErrorBase"
