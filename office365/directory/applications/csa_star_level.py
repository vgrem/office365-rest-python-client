from __future__ import annotations

from enum import Enum


class CsaStarLevel(Enum):
    none = "0"
    attestation = "1"
    certification = "2"
    continuousMonitoring = "3"
    cStarAssessment = "4"
    selfAssessment = "5"
    notSupported = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CsaStarLevel"
