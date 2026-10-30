from __future__ import annotations

from typing import AnyStr

from office365.entity import Entity
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata


class ChatMessageHostedContent(Entity):
    """Content in a chat or channel message hosted by Teams (e.g. an inline image)."""

    @odata(name="contentType")
    @property
    def content_type(self) -> str | None:
        """The media type of the hosted content (e.g. ``image/png``)."""
        return self.properties.get("contentType")

    def get_content(self) -> ClientResult[AnyStr]:
        """Download the hosted content bytes (``.../hostedContents/{id}/$value``)."""
        return_type = ClientResult[AnyStr](self.context)
        qry = FunctionQuery(self, "$value", None, return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.chatMessageHostedContent"
