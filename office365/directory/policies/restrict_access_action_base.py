from __future__ import annotations

from office365.security.datasecurity.dlp_action_info import DlpActionInfo
from office365.security.restrictionaction import RestrictionAction


class RestrictAccessActionBase(DlpActionInfo):
    restrictionAction: RestrictionAction = RestrictionAction.warn

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestrictAccessActionBase"
