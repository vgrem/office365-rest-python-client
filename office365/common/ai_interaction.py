from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.copilot.ai_interaction_attachment import AiInteractionAttachment
    from office365.copilot.ai_interaction_context import AiInteractionContext
    from office365.copilot.ai_interaction_link import AiInteractionLink
    from office365.copilot.ai_interaction_mention import AiInteractionMention
    from office365.directory.identity_set import IdentitySet
    from office365.outlook.mail.item_body import ItemBody
    from office365.teams.aiinteractions.interactiontype import AiInteractionType


class AiInteraction(Entity):
    @odata(name="appClass")
    @property
    def app_class(self) -> Optional[str]:
        """Gets the appClass property"""
        return self.properties.get("appClass", None)

    @odata(name="attachments")
    @property
    def attachments(self) -> ClientValueCollection[AiInteractionAttachment]:
        """Gets the attachments property"""
        from office365.copilot.ai_interaction_attachment import AiInteractionAttachment

        return self.properties.get(
            "attachments", ClientValueCollection[AiInteractionAttachment](AiInteractionAttachment)
        )

    @odata(name="body")
    @property
    def body(self) -> ItemBody:
        """Gets the body property"""
        from office365.outlook.mail.item_body import ItemBody

        return self.properties.get("body", ItemBody())

    @odata(name="contexts")
    @property
    def contexts(self) -> ClientValueCollection[AiInteractionContext]:
        """Gets the contexts property"""
        from office365.copilot.ai_interaction_context import AiInteractionContext

        return self.properties.get("contexts", ClientValueCollection[AiInteractionContext](AiInteractionContext))

    @odata(name="conversationType")
    @property
    def conversation_type(self) -> Optional[str]:
        """Gets the conversationType property"""
        return self.properties.get("conversationType", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="etag")
    @property
    def etag(self) -> Optional[str]:
        """Gets the etag property"""
        return self.properties.get("etag", None)

    @odata(name="from")
    @property
    def from_(self) -> IdentitySet:
        """Gets the from property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("from", IdentitySet())

    @odata(name="interactionType")
    @property
    def interaction_type(self) -> AiInteractionType:
        """Gets the interactionType property"""
        from office365.teams.aiinteractions.interactiontype import AiInteractionType

        return self.properties.get("interactionType", AiInteractionType.userPrompt)

    @odata(name="links")
    @property
    def links(self) -> ClientValueCollection[AiInteractionLink]:
        """Gets the links property"""
        from office365.copilot.ai_interaction_link import AiInteractionLink

        return self.properties.get("links", ClientValueCollection[AiInteractionLink](AiInteractionLink))

    @odata(name="locale")
    @property
    def locale(self) -> Optional[str]:
        """Gets the locale property"""
        return self.properties.get("locale", None)

    @odata(name="mentions")
    @property
    def mentions(self) -> ClientValueCollection[AiInteractionMention]:
        """Gets the mentions property"""
        from office365.copilot.ai_interaction_mention import AiInteractionMention

        return self.properties.get("mentions", ClientValueCollection[AiInteractionMention](AiInteractionMention))

    @odata(name="requestId")
    @property
    def request_id(self) -> Optional[str]:
        """Gets the requestId property"""
        return self.properties.get("requestId", None)

    @odata(name="sessionId")
    @property
    def session_id(self) -> Optional[str]:
        """Gets the sessionId property"""
        return self.properties.get("sessionId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteraction"
