from typing import Optional

from office365.entity import Entity
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.predicates import MessageRulePredicates
from office365.runtime.types.odata_property import odata


class MessageRule(Entity):
    """A rule that applies to messages in the Inbox of a user.

    In Outlook, you can set up rules for incoming messages in the Inbox to carry out specific internal
    upon certain conditions."""

    @odata(name="actions", persist=True)
    @property
    def actions(self) -> MessageRuleActions:
        """Actions to be taken on a message when the corresponding conditions are fulfilled."""
        return self.properties.get("actions", MessageRuleActions())

    @odata(name="conditions")
    @property
    def conditions(self) -> MessageRulePredicates:
        """Conditions that when fulfilled, will trigger the corresponding actions for that rule."""
        return self.properties.get("conditions", MessageRulePredicates())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """The display name of the rule."""
        return self.properties.get("displayName", None)

    @odata(name="exceptions")
    @property
    def exceptions(self) -> MessageRulePredicates:
        """Exception conditions for the rule."""
        return self.properties.get("exceptions", MessageRulePredicates())

    @odata(name="hasError")
    @property
    def has_error(self) -> Optional[bool]:
        """Indicates whether the rule is in an error condition."""
        return self.properties.get("hasError", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Indicates whether the rule is enabled to be applied to messages."""
        return self.properties.get("isEnabled", None)

    @property
    def is_read_only(self) -> Optional[bool]:
        """Indicates if the rule is read-only and cannot be modified or deleted by the rules REST API."""
        return self.properties.get("isReadOnly", None)

    @odata(name="sequence")
    @property
    def sequence(self) -> Optional[int]:
        """Indicates the order in which the rule is run, among other rules."""
        return self.properties.get("sequence", None)
