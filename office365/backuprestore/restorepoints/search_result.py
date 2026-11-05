from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from office365.common.restore_point import RestorePoint


class RestorePointSearchResult(ClientValue):
    artifactHitCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestorePointSearchResult"

    restorePoint: RestorePoint | None = None
