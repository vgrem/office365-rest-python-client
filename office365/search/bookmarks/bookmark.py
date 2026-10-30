from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.intune.devices.platformtype import DevicePlatformType
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.search.answers.answer import SearchAnswer
from office365.search.answers.state import AnswerState

if TYPE_CHECKING:
    from office365.search.answers.keyword import AnswerKeyword
    from office365.search.answers.variant import AnswerVariant


class Bookmark(SearchAnswer):
    """Represents a bookmark that is an administrative answer in Microsoft Search results for common search queries
    in an organization. A bookmark has many properties that allow administrators to make common resources more
    accessible in their organization."""

    @odata(name="availabilityEndDateTime")
    @property
    def availability_end_date_time(self) -> Optional[datetime]:
        """Gets the availabilityEndDateTime property"""
        return self.properties.get("availabilityEndDateTime", datetime.min)

    @odata(name="availabilityStartDateTime")
    @property
    def availability_start_date_time(self) -> Optional[datetime]:
        """Gets the availabilityStartDateTime property"""
        return self.properties.get("availabilityStartDateTime", datetime.min)

    @odata(name="categories")
    @property
    def categories(self) -> StringCollection:
        """Gets the categories property"""
        return self.properties.get("categories", StringCollection(None))

    @odata(name="groupIds")
    @property
    def group_ids(self) -> StringCollection:
        """Gets the groupIds property"""
        return self.properties.get("groupIds", StringCollection(None))

    @odata(name="isSuggested")
    @property
    def is_suggested(self) -> Optional[bool]:
        """Gets the isSuggested property"""
        return self.properties.get("isSuggested", None)

    @odata(name="languageTags")
    @property
    def language_tags(self) -> StringCollection:
        """Gets the languageTags property"""
        return self.properties.get("languageTags", StringCollection(None))

    @odata(name="platforms")
    @property
    def platforms(self) -> ClientValueCollection[DevicePlatformType]:
        """Gets the platforms property"""
        return self.properties.get("platforms", ClientValueCollection[DevicePlatformType](DevicePlatformType))

    @odata(name="powerAppIds")
    @property
    def power_app_ids(self) -> StringCollection:
        """Gets the powerAppIds property"""
        return self.properties.get("powerAppIds", StringCollection(None))

    @odata(name="state")
    @property
    def state(self) -> AnswerState:
        """Gets the state property"""
        return self.properties.get("state", AnswerState.published)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.search.Bookmark"

    @odata(name="keywords")
    @property
    def keywords(self) -> AnswerKeyword:
        """Gets the keywords property"""
        from office365.search.answers.keyword import AnswerKeyword

        return self.properties.get("keywords", AnswerKeyword())

    @odata(name="targetedVariations")
    @property
    def targeted_variations(self) -> ClientValueCollection[AnswerVariant]:
        """Gets the targetedVariations property"""
        from office365.search.answers.variant import AnswerVariant

        return self.properties.get("targetedVariations", ClientValueCollection[AnswerVariant](AnswerVariant))
