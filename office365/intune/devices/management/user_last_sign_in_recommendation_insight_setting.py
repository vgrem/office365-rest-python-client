from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.audit.usersigninrecommendationscope import (
    UserSignInRecommendationScope,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.runtime.types.duration import timedelta


@value
class UserLastSignInRecommendationInsightSetting(ClientValue):
    recommendationLookBackDuration: timedelta | None = None
    signInScope: UserSignInRecommendationScope = UserSignInRecommendationScope.tenant

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserLastSignInRecommendationInsightSetting"
