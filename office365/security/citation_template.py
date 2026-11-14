from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.security.file_plan_descriptor_template import FilePlanDescriptorTemplate


class CitationTemplate(FilePlanDescriptorTemplate):
    @odata(name="citationJurisdiction")
    @property
    def citation_jurisdiction(self) -> Optional[str]:
        """Gets the citationJurisdiction property"""
        return self.properties.get("citationJurisdiction", None)

    @odata(name="citationUrl")
    @property
    def citation_url(self) -> Optional[str]:
        """Gets the citationUrl property"""
        return self.properties.get("citationUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.CitationTemplate"
