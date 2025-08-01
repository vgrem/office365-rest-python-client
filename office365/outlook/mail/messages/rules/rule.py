from typing import Optional

from office365.entity import Entity
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.predicates import MessageRulePredicates
from office365.runtime.client_object_meta import persist_property


class MessageRule(Entity):
    """A rule that applies to messages in the Inbox of a user.

    In Outlook, you can set up rules for incoming messages in the Inbox to carry out specific internal
    upon certain conditions."""

    @property
    @persist_property()
    def actions(self) -> MessageRuleActions:
        """Actions to be taken on a message when the corresponding conditions are fulfilled."""
        return self.properties.get("actions", MessageRuleActions())

    @property
    def conditions(self) -> MessageRulePredicates:
        """Conditions that when fulfilled, will trigger the corresponding actions for that rule."""
        return self.properties.get("conditions", MessageRulePredicates())

    @property
    def exceptions(self) -> MessageRulePredicates:
        """Exception conditions for the rule."""
        return self.properties.get("exceptions", MessageRulePredicates())

    @property
    def is_read_only(self) -> Optional[bool]:
        """Indicates if the rule is read-only and cannot be modified or deleted by the rules REST API."""
        return self.properties.get("isReadOnly", None)
