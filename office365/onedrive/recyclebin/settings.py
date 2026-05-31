from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RecycleBinSettings(ClientValue):
    """Represents settings for the recycleBin resource type."""

    retentionPeriodOverrideDays: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecycleBinSettings"
