from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.recommendation_insight_setting import (
    AccessReviewRecommendationInsightSetting as ReviewRecommendationInsightSetting,
)
from office365.directory.identitygovernance.accessreview.reviewer_scope import AccessReviewReviewerScope
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class AccessReviewStageSettings(ClientValue):
    decisionsThatWillMoveToNextStage: StringCollection = field(default_factory=StringCollection)
    dependsOn: StringCollection = field(default_factory=StringCollection)
    durationInDays: int | None = None
    fallbackReviewers: ClientValueCollection[AccessReviewReviewerScope] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewReviewerScope)
    )
    recommendationInsightSettings: ClientValueCollection[ReviewRecommendationInsightSetting] = field(
        default_factory=lambda: ClientValueCollection(ReviewRecommendationInsightSetting)
    )
    recommendationsEnabled: bool | None = None
    reviewers: ClientValueCollection[AccessReviewReviewerScope] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewReviewerScope)
    )
    stageId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewStageSettings"
