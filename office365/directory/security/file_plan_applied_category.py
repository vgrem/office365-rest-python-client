from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.file_plan_subcategory import FilePlanSubcategory
from office365.runtime.client_value import ClientValue


@dataclass
class FilePlanAppliedCategory(ClientValue):
    subcategory: FilePlanSubcategory = field(default_factory=FilePlanSubcategory)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FilePlanAppliedCategory"
