from __future__ import annotations

from enum import Enum


class CrossTenantMigrationJobType(Enum):
    validate = "0"
    migrate = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationJobType"
