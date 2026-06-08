from typing import Any

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.rule import MessageRule


class MessageRuleCollection(EntityCollection[MessageRule]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, MessageRule, resource_path)

    @require_permission(delegated=["Mail.ReadWrite"], application=["Mail.ReadWrite"])
    def add(self, display_name: str, sequence: int, actions: MessageRuleActions, **kwargs: Any) -> MessageRule:
        """Create a messageRule object by specifying a set of conditions and actions.
        Outlook carries out those actions if an incoming message in the user's Inbox meets the specified conditions.
        This API is available in the following national cloud deployments.

        Args:
            display_name (str): The display name of the rule.
            sequence (int): Indicates the order in which the rule is executed, among other rules.
            actions (MessageRuleActions): Actions to be taken on a message when the corresponding conditions, if any, are fulfilled.
        """
        props = {
            "displayName": display_name,
            "sequence": sequence,
            "actions": actions.to_json(),
            **kwargs,
        }
        return super().add(**props)
