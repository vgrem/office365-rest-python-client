from __future__ import annotations

from dataclasses import field

from office365.security.labels.file_plan_descriptor_base import FilePlanDescriptorBase
from office365.security.labels.file_plan_subcategory import FilePlanSubcategory


class FilePlanAppliedCategory(FilePlanDescriptorBase):
    subcategory: FilePlanSubcategory = field(default_factory=FilePlanSubcategory)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FilePlanAppliedCategory"
