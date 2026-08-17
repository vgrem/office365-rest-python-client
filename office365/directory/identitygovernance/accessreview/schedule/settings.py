from __future__ import annotations

from dataclasses import field
from datetime import timedelta

from office365.directory.identitygovernance.accessreview.apply_action import AccessReviewApplyAction
from office365.directory.identitygovernance.accessreview.recommendation_insight_setting import (
    AccessReviewRecommendationInsightSetting,
)
from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class AccessReviewScheduleSettings(ClientValue):
    applyActions: ClientValueCollection[AccessReviewApplyAction] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewApplyAction)
    )
    autoApplyDecisionsEnabled: bool | None = None
    decisionHistoriesForReviewersEnabled: bool | None = None
    defaultDecision: str | None = None
    defaultDecisionEnabled: bool | None = None
    instanceDurationInDays: int | None = None
    justificationRequiredOnApproval: bool | None = None
    mailNotificationsEnabled: bool | None = None
    recommendationInsightSettings: ClientValueCollection[AccessReviewRecommendationInsightSetting] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewRecommendationInsightSetting)
    )
    recommendationLookBackDuration: timedelta | None = None
    recommendationsEnabled: bool | None = None
    recurrence: PatternedRecurrence = field(default_factory=PatternedRecurrence)
    reminderNotificationsEnabled: bool | None = None
    "The accessReviewScheduleSettings defines the settings of an accessReviewScheduleDefinition."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewScheduleSettings"
