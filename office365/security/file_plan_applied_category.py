from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.file_plan_subcategory import FilePlanSubcategory


@value
class FilePlanAppliedCategory(ClientValue):
    subcategory: FilePlanSubcategory = field(default_factory=FilePlanSubcategory)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FilePlanAppliedCategory"
