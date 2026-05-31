from __future__ import annotations

from dataclasses import dataclass

from office365.onenote.patchactiontype import OnenotePatchActionType
from office365.onenote.patchinsertposition import OnenotePatchInsertPosition
from office365.runtime.client_value import ClientValue


@dataclass
class OnenotePatchContentCommand(ClientValue):
    action: OnenotePatchActionType = OnenotePatchActionType.Replace
    content: str | None = None
    position: OnenotePatchInsertPosition = OnenotePatchInsertPosition.After
    target: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenotePatchContentCommand"
