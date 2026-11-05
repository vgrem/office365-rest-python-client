from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.datasecurity.classifcation_error_base import (
    ClassifcationErrorBase,
)


class ClassificationError(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ClassificationError"

    details: ClientValueCollection[ClassifcationErrorBase] = field(
        default_factory=lambda: ClientValueCollection(ClassifcationErrorBase)
    )
