from __future__ import annotations

from dataclasses import field

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.stream import Stream
from office365.security.threatintelligence.geo_location import GeoLocation


class IpEvidence(AlertEvidence):
    countryLetterCode: str | None = None
    ipAddress: str | None = None
    stream: Stream = field(default_factory=Stream)
    location: GeoLocation = field(default_factory=GeoLocation)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IpEvidence"
