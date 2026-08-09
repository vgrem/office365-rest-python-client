from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.restrictionaction import RestrictionAction
from office365.runtime.client_value import ClientValue


@dataclass
class RestrictAccessActionBase(ClientValue):
    restrictionAction: RestrictionAction = RestrictionAction.warn

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestrictAccessActionBase"
