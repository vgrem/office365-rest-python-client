from __future__ import annotations

from office365.copilot.action_result_part import ActionResultPart


class AadUserConversationMemberResult(ActionResultPart):
    userId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AadUserConversationMemberResult"
