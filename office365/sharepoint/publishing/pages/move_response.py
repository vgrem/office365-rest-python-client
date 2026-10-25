from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.publishing.pagedeepcopywarning import PageDeepCopyWarning


class PageMoveResponse(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "SP.Publishing.PageMoveResponse"

    @odata(name="CompletedAssets")
    @property
    def completed_assets(self) -> StringCollection:
        """Gets the CompletedAssets property"""
        return self.properties.get("CompletedAssets", StringCollection())

    @odata(name="ErrorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="ErrorType")
    @property
    def error_type(self) -> Optional[int]:
        """Gets the ErrorType property"""
        return self.properties.get("ErrorType", None)

    @odata(name="JobState")
    @property
    def job_state(self) -> Optional[int]:
        """Gets the JobState property"""
        return self.properties.get("JobState", None)

    @odata(name="NewPageId")
    @property
    def new_page_id(self) -> Optional[int]:
        """Gets the NewPageId property"""
        return self.properties.get("NewPageId", None)

    @odata(name="NewPageUniqueId")
    @property
    def new_page_unique_id(self) -> Optional[UUID]:
        """Gets the NewPageUniqueId property"""
        return self.properties.get("NewPageUniqueId", None)

    @odata(name="NewPageUrl")
    @property
    def new_page_url(self) -> Optional[str]:
        """Gets the NewPageUrl property"""
        return self.properties.get("NewPageUrl", None)

    @odata(name="TotalAssetsToMove")
    @property
    def total_assets_to_move(self) -> Optional[int]:
        """Gets the TotalAssetsToMove property"""
        return self.properties.get("TotalAssetsToMove", None)

    @odata(name="Warnings")
    @property
    def warnings(self) -> ClientValueCollection[PageDeepCopyWarning]:
        """Gets the Warnings property"""
        from office365.sharepoint.publishing.pagedeepcopywarning import (
            PageDeepCopyWarning,
        )

        return self.properties.get("Warnings", ClientValueCollection[PageDeepCopyWarning](PageDeepCopyWarning))

    @odata(name="WorkItemId")
    @property
    def work_item_id(self) -> Optional[UUID]:
        """Gets the WorkItemId property"""
        return self.properties.get("WorkItemId", None)
