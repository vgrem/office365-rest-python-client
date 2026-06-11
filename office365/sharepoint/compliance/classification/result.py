from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class ClassificationResult(ClientValue):
    ConfidenceScore: float | None = None
    ContentTypeId: str | None = None
    ContentTypeName: str | None = None
    Error: str | None = None
    Metas: dict | None = field(default_factory=dict)
    ModelId: str | None = None
    ModelVersion: str | None = None
    RetentionLabelFlags: int | None = None
    RetentionLabelName: str | None = None
    RetryCount: int | None = None
    SensitivityLabel: str | None = None
    TableMetas: dict | None = field(default_factory=dict)
