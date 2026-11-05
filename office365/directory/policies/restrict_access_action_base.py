from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.restrictionaction import RestrictionAction


class RestrictAccessActionBase(ClientValue):
    restrictionAction: RestrictionAction = RestrictionAction.warn

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestrictAccessActionBase"
