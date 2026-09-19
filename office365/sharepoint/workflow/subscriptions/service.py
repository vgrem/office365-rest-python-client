from __future__ import annotations

from uuid import UUID

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class WorkflowSubscriptionService(Entity):
    @property
    def current(self) -> WorkflowSubscriptionService:
        """Gets the Current property"""
        return self.properties.get(
            "Current", WorkflowSubscriptionService(self.context, ResourcePath("Current", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowSubscriptionService"

    def delete_subscription(self, subscription_id: UUID) -> Self:
        """DeleteSubscription operation.

        Args:
            subscription_id (UUID): subscriptionId parameter
        """
        qry = ServiceOperationQuery(self, "DeleteSubscription", None, {"subscriptionId": subscription_id}, None, None)
        self.context.add_query(qry)
        return self

    def register_interest_in_host_web_list(self, list_id: UUID, event_name: str) -> Self:
        """RegisterInterestInHostWebList operation.

        Args:
            list_id (UUID): listId parameter
            event_name (str): eventName parameter
        """
        qry = ServiceOperationQuery(
            self, "RegisterInterestInHostWebList", None, {"listId": list_id, "eventName": event_name}, None, None
        )
        self.context.add_query(qry)
        return self

    def register_interest_in_list(self, list_id: UUID, event_name: str) -> Self:
        """RegisterInterestInList operation.

        Args:
            list_id (UUID): listId parameter
            event_name (str): eventName parameter
        """
        qry = ServiceOperationQuery(
            self, "RegisterInterestInList", None, {"listId": list_id, "eventName": event_name}, None, None
        )
        self.context.add_query(qry)
        return self

    def unregister_interest_in_host_web_list(self, list_id: UUID, event_name: str) -> Self:
        """UnregisterInterestInHostWebList operation.

        Args:
            list_id (UUID): listId parameter
            event_name (str): eventName parameter
        """
        qry = ServiceOperationQuery(
            self, "UnregisterInterestInHostWebList", None, {"listId": list_id, "eventName": event_name}, None, None
        )
        self.context.add_query(qry)
        return self

    def unregister_interest_in_list(self, list_id: UUID, event_name: str) -> Self:
        """UnregisterInterestInList operation.

        Args:
            list_id (UUID): listId parameter
            event_name (str): eventName parameter
        """
        qry = ServiceOperationQuery(
            self, "UnregisterInterestInList", None, {"listId": list_id, "eventName": event_name}, None, None
        )
        self.context.add_query(qry)
        return self
