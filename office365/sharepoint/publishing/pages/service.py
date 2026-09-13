from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.administration.orgassets.org_assets import OrgAssets
from office365.sharepoint.clientsidecomponent.query_result import SPClientSideComponentQueryResult
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.files.file import File
from office365.sharepoint.publishing.campaign.campaign import Campaign
from office365.sharepoint.publishing.file_picker_options import FilePickerOptions
from office365.sharepoint.publishing.gettyimage import GettyImage
from office365.sharepoint.publishing.pages.collection import SitePageCollection
from office365.sharepoint.publishing.pages.page import SitePage
from office365.sharepoint.publishing.primary_city_time import PrimaryCityTime
from office365.sharepoint.publishing.sites.communication.site import CommunicationSite

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class SitePageService(Entity):
    """Represents a set of APIs to use for managing site pages."""

    def __init__(self, context, resource_path=None):
        """Represents a set of APIs to use for managing site pages."""
        if resource_path is None:
            resource_path = ResourcePath("SP.Publishing.SitePageService")
        super().__init__(context, resource_path)

    @property
    def pages(self) -> SitePageCollection:
        """Gets the SitePageCollection for the current web."""
        return self.properties.get("pages", SitePageCollection(self.context, ResourcePath("pages", self.resource_path)))

    @odata(name="CommunicationSite")
    @property
    def communication_site(self) -> CommunicationSite:
        """Gets a CommunicationSite for the current web."""
        return self.properties.get(
            "CommunicationSite", CommunicationSite(self.context, ResourcePath("CommunicationSite", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageService"

    @property
    def custom_content_approval_enabled(self) -> Optional[bool]:
        """Gets the CustomContentApprovalEnabled property"""
        return self.properties.get("CustomContentApprovalEnabled", None)

    @property
    def campaigns(self) -> EntityCollection[Campaign]:
        """Gets the Campaigns property"""
        return self.properties.get(
            "Campaigns",
            EntityCollection[Campaign](self.context, Campaign, ResourcePath("Campaigns", self.resource_path)),
        )

    def create_page(self, title: str, language: Optional[str] = None) -> SitePage:
        """Create a new sitePage in the site pages list in a site.

        Args:
            title (str): The title of Site Page
            language (str): The language of the Site Page.
        """

        def _page_created(return_type: SitePage) -> None:
            def _draft_saved(result: ClientResult[bool]) -> None:
                return_type.get()

            return_type.save_draft(title=title).after_execute(_draft_saved, execute_first=True)

        return self.pages.add().after_execute(_page_created)

    def create_and_publish_page(self, title):
        """Create and publish a new sitePage in the site pages list in a site.

        Args:
            title (str): The title of Site Page
        """

        def _page_created(return_type: SitePage) -> None:
            def _page_published(result: ClientResult[bool]) -> None:
                pass

            return_type.publish().after_execute(_page_published)

        return self.create_page(title).after_execute(_page_created)

    def can_create_page(self) -> ClientResult[bool]:
        """
        Checks if the current user has permission to create a site page on the site pages document library.
        MUST return true if the user has permission to create a site page, otherwise MUST return false.
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "CanCreatePage", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def can_create_promoted_page(self) -> ClientResult[bool]:
        """
        Checks if the current user has permission to create a site page on the site pages document library.
        MUST return true if the user has permission to create a site page, otherwise MUST return false.
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "CanCreatePromotedPage", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @staticmethod
    def get_current_user_memberships(
        context: ClientContext, scenario: Optional[str] = None
    ) -> ClientResult[StringCollection]:
        return_type = ClientResult(context, StringCollection())
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "GetCurrentUserMemberships", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_time_zone(context: ClientContext, city_name: str) -> PrimaryCityTime:
        """Gets time zone data for specified city.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            city_name (str): The name of the city.
        """
        return_type = PrimaryCityTime(context)
        binding_type = SitePageService(context)
        params = {"cityName": city_name}
        qry = ServiceOperationQuery(binding_type, "GetTimeZone", params, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def compute_file_name(context: ClientContext, title: str) -> ClientResult[str]:
        """Args:
        context (office365.sharepoint.client_context.ClientContext): Client context
        title (str): The title of the page.
        """
        return_type = ClientResult[str](context)
        binding_type = SitePageService(context)
        params = {"title": title}
        qry = ServiceOperationQuery(binding_type, "ComputeFileName", params, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_available_full_page_applications(context, include_errors=None, project=None):
        return_type = ClientResult(context, ClientValueCollection(SPClientSideComponentQueryResult))
        params = {"includeErrors": include_errors, "project": project}
        qry = ServiceOperationQuery(
            SitePageService(context), "GetAvailableFullPageApplications", None, params, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def is_file_picker_external_image_search_enabled(context: ClientContext) -> ClientResult[bool]:
        return_type = ClientResult[bool](context)
        binding_type = SitePageService(context)
        qry = ServiceOperationQuery(
            binding_type, "IsFilePickerExternalImageSearchEnabled", None, None, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def org_assets(context: ClientContext) -> ClientResult[OrgAssets]:
        return_type = ClientResult(context, OrgAssets())
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "OrgAssets", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def file_picker_tab_options(context: ClientContext) -> ClientResult[FilePickerOptions]:
        return_type = ClientResult(context, FilePickerOptions())
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "FilePickerTabOptions", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    def add_image(self, page_name, image_file_name, image_stream):
        """Adds an image to the site assets library of the current web.
        Returns a File object ([MS-CSOMSPT] section 3.2.5.64) that represents the image.

        Args:
            image_stream (str): The image stream.
            image_file_name (str): Indicates the file name of the image to be added.
            page_name (str): Indicates the name of that site page that the image is to be used in.
        Returns:
            File
        """
        return_type = File(self.context)
        params = {"pageName": page_name, "imageFileName": image_file_name, "imageStream": image_stream}
        qry = ServiceOperationQuery(self, "AddImage", params, None, None, return_type, True)
        self.context.add_query(qry)
        return return_type

    def add_image_from_external_url(self, page_name, image_file_name, external_url, sub_folder_name, page_id):
        """Adds an image to the site assets library of the current web.
        Returns a File object ([MS-CSOMSPT] section 3.2.5.64) that represents the image.

        Args:
            image_file_name (str): Indicates the file name of the image to be added.
            page_name (str): Indicates the name of that site page that the image is to be used in.
            external_url (str):
            sub_folder_name (str):
            page_id (str):
        """
        return_type = File(self.context)
        params = {
            "pageName": page_name,
            "imageFileName": image_file_name,
            "externalUrl": external_url,
            "subFolderName": sub_folder_name,
            "pageId": page_id,
        }
        qry = ServiceOperationQuery(self, "AddImageFromExternalUrl", params, None, None, return_type)
        qry.static = True
        self.context.add_query(qry)
        return return_type

    def enable_amplify_from_anywhere(self) -> Self:
        """EnableAmplifyFromAnywhere operation."""
        qry = ServiceOperationQuery(self, "EnableAmplifyFromAnywhere", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def enable_announcements(self) -> Self:
        """EnableAnnouncements operation."""
        qry = ServiceOperationQuery(self, "EnableAnnouncements", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def enable_categories(self) -> Self:
        """EnableCategories operation."""
        qry = ServiceOperationQuery(self, "EnableCategories", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def enable_lightweight_campaign(self) -> Self:
        """EnableLightweightCampaign operation."""
        qry = ServiceOperationQuery(self, "EnableLightweightCampaign", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def get_or_create_asset_folder(
        self, page_name: str, create_folder_if_needed: bool, sub_folder_name: str, page_id: int
    ) -> ClientResult[str]:
        """GetOrCreateAssetFolder operation.

        Args:
            page_name (str): pageName parameter
            create_folder_if_needed (bool): createFolderIfNeeded parameter
            sub_folder_name (str): subFolderName parameter
            page_id (int): pageId parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "GetOrCreateAssetFolder",
            None,
            {
                "pageName": page_name,
                "createFolderIfNeeded": create_folder_if_needed,
                "subFolderName": sub_folder_name,
                "pageId": page_id,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def report_getty_images(self, images: ClientValueCollection[GettyImage], is_timer_job: bool) -> ClientResult[bool]:
        """ReportGettyImages operation.

        Args:
            images (ClientValueCollection[GettyImage]): images parameter
            is_timer_job (bool): isTimerJob parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(
            self, "ReportGettyImages", None, {"images": images, "isTimerJob": is_timer_job}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
