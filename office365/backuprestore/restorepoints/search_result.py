from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.common.restore_point import RestorePoint


@value
class RestorePointSearchResult(ClientValue):
    artifactHitCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestorePointSearchResult"

    restorePoint: RestorePoint | None = None
