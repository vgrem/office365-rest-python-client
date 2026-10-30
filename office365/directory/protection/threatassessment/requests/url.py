from __future__ import annotations

from typing import Optional

from office365.directory.protection.threatassessment.requests.request import (
    ThreatAssessmentRequest,
)
from office365.runtime.types.odata_property import odata


class UrlAssessmentRequest(ThreatAssessmentRequest):
    """
    Used to create and retrieve a URL threat assessment, derived from threatAssessmentRequest.
    """

    @odata(name="url")
    @property
    def url(self) -> Optional[str]:
        """The URL string to assess."""
        return self.properties.get("url", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.urlAssessmentRequest"
