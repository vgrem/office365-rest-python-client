from __future__ import annotations

from office365.security.file_plan_descriptor_base import FilePlanDescriptorBase


class FilePlanCitation(FilePlanDescriptorBase):
    citationJurisdiction: str | None = None
    citationUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FilePlanCitation"
