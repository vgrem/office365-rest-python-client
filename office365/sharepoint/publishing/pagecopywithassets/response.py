from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.pagedeepcopywarning import PageDeepCopyWarning


class PageCopyResponse(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.PageCopyWithAssets.PageCopyResponse"

    @odata(name="CanvasString")
    @property
    def canvas_string(self) -> Optional[str]:
        """Gets the CanvasString property"""
        return self.properties.get("CanvasString", None)

    @odata(name="CompletedAssets")
    @property
    def completed_assets(self) -> StringCollection:
        """Gets the CompletedAssets property"""
        return self.properties.get("CompletedAssets", StringCollection())

    @odata(name="CopyToStatusAPI")
    @property
    def copy_to_status_api(self) -> Optional[str]:
        """Gets the CopyToStatusAPI property"""
        return self.properties.get("CopyToStatusAPI", None)

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

    @odata(name="NewPageVersion")
    @property
    def new_page_version(self) -> Optional[str]:
        """Gets the NewPageVersion property"""
        return self.properties.get("NewPageVersion", None)

    @odata(name="TotalAssetsToCopy")
    @property
    def total_assets_to_copy(self) -> Optional[int]:
        """Gets the TotalAssetsToCopy property"""
        return self.properties.get("TotalAssetsToCopy", None)

    @odata(name="Warnings")
    @property
    def warnings(self) -> ClientValueCollection[PageDeepCopyWarning]:
        """Gets the Warnings property"""
        return self.properties.get("Warnings", ClientValueCollection[PageDeepCopyWarning](PageDeepCopyWarning))

    @odata(name="WorkItemId")
    @property
    def work_item_id(self) -> Optional[UUID]:
        """Gets the WorkItemId property"""
        return self.properties.get("WorkItemId", None)
