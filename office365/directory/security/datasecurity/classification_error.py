from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.datasecurity.classifcation_error_base import ClassificationErrorBase
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ClassificationError(ClientValue):
    details: ClientValueCollection[ClassificationErrorBase] = field(
        default_factory=lambda: ClientValueCollection(ClassificationErrorBase)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ClassificationError"
