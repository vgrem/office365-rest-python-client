from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.accessreview.history.decisionfilter import (
    AccessReviewHistoryDecisionFilter,
)
from office365.directory.identitygovernance.accessreview.history.status import (
    AccessReviewHistoryStatus,
)
from office365.directory.identitygovernance.accessreview.history_instance import (
    AccessReviewHistoryInstance,
)
from office365.directory.identitygovernance.accessreview.history_schedule_settings import (  # noqa: E501
    AccessReviewHistoryScheduleSettings,
)
from office365.directory.identitygovernance.accessreview.scope import AccessReviewScope
from office365.directory.users.identity import UserIdentity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AccessReviewHistoryDefinition(Entity):
    """
    Represents a collection of access review historical data and the scopes used to collect that data.

    An accessReviewHistoryDefinition contains a list of accessReviewHistoryInstance objects.
    Each recurrence of the history definition creates an instance. In the case of a one-time history definition,
    only one instance is created.
    """

    @odata(name="scopes")
    @property
    def scopes(self):
        """
        Used to scope what reviews are included in the fetched history data. Fetches reviews whose scope matches with
        this provided scope. Required.
        """
        return self.properties.get("scopes", ClientValueCollection(AccessReviewScope))

    @odata(name="createdBy")
    @property
    def created_by(self) -> UserIdentity:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", UserIdentity())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="decisions")
    @property
    def decisions(self) -> ClientValueCollection[AccessReviewHistoryDecisionFilter]:
        """Gets the decisions property"""
        return self.properties.get(
            "decisions", ClientValueCollection[AccessReviewHistoryDecisionFilter](AccessReviewHistoryDecisionFilter)
        )

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="reviewHistoryPeriodEndDateTime")
    @property
    def review_history_period_end_date_time(self) -> datetime:
        """Gets the reviewHistoryPeriodEndDateTime property"""
        return self.properties.get("reviewHistoryPeriodEndDateTime", datetime.min)

    @odata(name="reviewHistoryPeriodStartDateTime")
    @property
    def review_history_period_start_date_time(self) -> datetime:
        """Gets the reviewHistoryPeriodStartDateTime property"""
        return self.properties.get("reviewHistoryPeriodStartDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> AccessReviewHistoryStatus:
        """Gets the status property"""
        return self.properties.get("status", AccessReviewHistoryStatus.done)

    @odata(name="instances", navigation=True)
    @property
    def instances(self) -> EntityCollection[AccessReviewHistoryInstance]:
        """Gets the instances property"""
        return self.properties.get(
            "instances",
            EntityCollection[AccessReviewHistoryInstance](
                self.context, AccessReviewHistoryInstance, ResourcePath("instances", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewHistoryDefinition"

    @odata(name="scheduleSettings")
    @property
    def schedule_settings(self) -> AccessReviewHistoryScheduleSettings:
        """Gets the scheduleSettings property"""
        return self.properties.get("scheduleSettings", AccessReviewHistoryScheduleSettings())
