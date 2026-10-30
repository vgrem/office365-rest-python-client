from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.suggestion_related_people_insight_level import (  # noqa: E501
        AccessPackageSuggestionRelatedPeopleInsightLevel,
    )


class EndUserSettings(Entity):
    @odata(name="relatedPeopleInsightLevel")
    @property
    def related_people_insight_level(self) -> AccessPackageSuggestionRelatedPeopleInsightLevel:
        """Gets the relatedPeopleInsightLevel property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.suggestion_related_people_insight_level import (  # noqa: E501
            AccessPackageSuggestionRelatedPeopleInsightLevel,
        )

        return self.properties.get(
            "relatedPeopleInsightLevel", AccessPackageSuggestionRelatedPeopleInsightLevel.disabled
        )

    @odata(name="showApproverDetailsToMembers")
    @property
    def show_approver_details_to_members(self) -> Optional[bool]:
        """Gets the showApproverDetailsToMembers property"""
        return self.properties.get("showApproverDetailsToMembers", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EndUserSettings"
