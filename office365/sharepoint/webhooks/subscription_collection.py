from __future__ import annotations

from datetime import datetime

from typing_extensions import Self

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.webhooks.subscription import Subscription
from office365.sharepoint.webhooks.subscription_information import (
    SubscriptionInformation,
)


class SubscriptionCollection(EntityCollection[Subscription]):
    """Represents a collection of Subscription (WebHook) resources."""

    def __init__(self, context, resource_path=None, parent=None):
        super().__init__(context, Subscription, resource_path, parent)

    def get_by_id(self, _id):
        """Gets the subscription with the specified ID."""
        return Subscription(self.context, ServiceOperationPath("getById", [_id], self.resource_path))

    def add(self, notification_url: str, expiration_date_time: datetime):
        """Args:
        notification_url (str): notification string
        expiration_date_time (datetime): Subscription expiration date
        """
        return_type = Subscription(self.context)
        self.add_child(return_type)

        def _add(resource: Entity):
            information = SubscriptionInformation(
                notificationUrl=notification_url,
                resource=resource.get_property("id"),
                expirationDateTime=expiration_date_time,
            )
            payload = {"parameters": information}
            qry = ServiceOperationQuery(self, "Add", None, payload, None, return_type)
            self.context.add_query(qry)

        assert self._parent is not None
        self._parent.ensure_property("Id").after_execute(_add)

        return return_type

    def remove(self, subscription_id: str) -> Self:
        """Removes the subscription with the specified subscriptionId from the collection.

        Args:
            subscription_id (str): The ID of the subscription.
        """
        payload = {
            "subscriptionId": subscription_id,
        }
        qry = ServiceOperationQuery(self, "Remove", payload, None, None, None)
        self.context.add_query(qry)
        return self
