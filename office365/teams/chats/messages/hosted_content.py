from __future__ import annotations

from typing import AnyStr

from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.teams.apps.teamwork_hosted_content import TeamworkHostedContent


class ChatMessageHostedContent(TeamworkHostedContent):
    """Content in a chat or channel message hosted by Teams (e.g. an inline image)."""

    @require_permission(
        delegated=["Chat.Read", "ChannelMessage.Read.All"],
        application=["ChatMessage.Read.All", "ChannelMessage.Read.All"],
        notes="Download the hosted content bytes",
    )
    def get_content(self) -> ClientResult[AnyStr]:
        """Download the hosted content bytes (``.../hostedContents/{id}/$value``)."""
        return_type = ClientResult[AnyStr](self.context)
        qry = FunctionQuery(self, "$value", None, return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.chatMessageHostedContent"
