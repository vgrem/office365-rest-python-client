from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.pages.version_info import SitePageVersionInfo
from office365.sharepoint.publishing.user_info import UserInfo

if TYPE_CHECKING:
    from office365.sharepoint.publishing.pages.metadata_collection import (
        SitePageMetadataCollection,
    )


class SitePageMetadata(Entity):
    """Represents the core properties of a Site Page."""

    def __repr__(self):
        return self.file_name or self.absolute_url or self.entity_type_name

    @odata(name="AbsoluteUrl", beta=True)
    @property
    def absolute_url(self) -> Optional[str]:
        """Gets the absolute Url of the Site Page."""
        return self.properties.get("AbsoluteUrl", None)

    @odata(name="AuthorByline", beta=True)
    @property
    def author_byline(self) -> StringCollection:
        return self.properties.get("AuthorByline", StringCollection())

    @odata(name="CreatedBy", navigation=True, beta=True)
    @property
    def created_by(self) -> UserInfo:
        """Specifies the user who created the page."""
        return self.properties.get("CreatedBy", UserInfo())

    @odata(name="LastModifiedBy", navigation=True, beta=True)
    @property
    def last_modified_by(self) -> UserInfo:
        """Gets the user who last modified the current Site Page."""
        return self.properties.get("LastModifiedBy", UserInfo())

    @odata(name="CommentsDisabled", beta=True)
    @property
    def comments_disabled(self) -> Optional[bool]:
        """Indicates if comments are disabled for the current Site Page."""
        return self.properties.get("CommentsDisabled", None)

    @odata(name="BannerImageUrl", beta=True)
    @property
    def banner_image_url(self) -> Optional[str]:
        """Gets the banner image Url"""
        return self.properties.get("BannerImageUrl", None)

    @banner_image_url.setter
    def banner_image_url(self, value: str) -> None:
        """Sets the banner image Url"""
        self.set_property("BannerImageUrl", value)

    @odata(name="ContentTypeId", beta=True)
    @property
    def content_type_id(self) -> Optional[str]:
        """Gets the content type ID of the current Site Page."""
        return self.properties.get("ContentTypeId", None)

    @content_type_id.setter
    def content_type_id(self, value: str) -> None:
        """Sets the content type ID of the current Site Page."""
        self.set_property("ContentTypeId", value)

    @odata(name="Description", beta=True)
    @property
    def description(self) -> Optional[str]:
        """Gets the description for the current Site Page"""
        return self.properties.get("Description", None)

    @odata(name="DoesUserHaveEditPermission", beta=True)
    @property
    def does_user_have_edit_permission(self) -> Optional[bool]:
        """Indicates if the current user has edit permission to the Site Page."""
        return self.properties.get("DoesUserHaveEditPermission", None)

    @odata(name="FileName", beta=True)
    @property
    def file_name(self) -> Optional[str]:
        """Gets the file name of the current Site Page."""
        return self.properties.get("FileName", None)

    @odata(name="FirstPublished", beta=True)
    @property
    def first_published(self) -> Optional[datetime.datetime]:
        """Datetime of when the site page was initially published.
        The server MUST return Datetime.MinValue (00:00:00:0000000 UTC) when the site page has never been published.
        """
        return self.properties.get("FirstPublished", None)

    @odata(name="IsPageCheckedOutToCurrentUser", beta=True)
    @property
    def is_page_checked_out_to_current_user(self) -> Optional[bool]:
        """Indicates if the Site Page is checked out to the current user."""
        return self.properties.get("IsPageCheckedOutToCurrentUser", None)

    @odata(name="VersionInfo", beta=True)
    @property
    def version_info(self) -> SitePageVersionInfo:
        """Gets the version information for the most recently checked in version of the Site Page."""
        return self.properties.get("VersionInfo", SitePageVersionInfo())

    @property
    def parent_collection(self) -> SitePageMetadataCollection:
        from office365.sharepoint.publishing.pages.metadata_collection import (
            SitePageMetadataCollection,
        )

        return cast(SitePageMetadataCollection, self._parent_collection)

    @odata(name="TopicHeader", beta=True)
    @property
    def topic_header(self) -> Optional[str]:
        return self.properties.get("TopicHeader", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.SitePageMetadata"

    @odata(name="AssetFolderId", beta=True)
    @property
    def asset_folder_id(self) -> Optional[int]:
        """Gets the AssetFolderId property"""
        return self.properties.get("AssetFolderId", None)

    @odata(name="BannerThumbnailUrl", beta=True)
    @property
    def banner_thumbnail_url(self) -> Optional[str]:
        """Gets the BannerThumbnailUrl property"""
        return self.properties.get("BannerThumbnailUrl", None)

    @odata(name="CallToAction", beta=True)
    @property
    def call_to_action(self) -> Optional[str]:
        """Gets the CallToAction property"""
        return self.properties.get("CallToAction", None)

    @odata(name="Categories", beta=True)
    @property
    def categories(self) -> Optional[str]:
        """Gets the Categories property"""
        return self.properties.get("Categories", None)

    @odata(name="CommentCount", beta=True)
    @property
    def comment_count(self) -> Optional[int]:
        """Gets the CommentCount property"""
        return self.properties.get("CommentCount", None)

    @odata(name="Created", beta=True)
    @property
    def created(self) -> Optional[datetime.datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.datetime.min)

    @odata(name="FirstPublishedRelativeTime", beta=True)
    @property
    def first_published_relative_time(self) -> Optional[str]:
        """Gets the FirstPublishedRelativeTime property"""
        return self.properties.get("FirstPublishedRelativeTime", None)

    @odata(name="HasUserRecentlyModified", beta=True)
    @property
    def has_user_recently_modified(self) -> Optional[bool]:
        """Gets the HasUserRecentlyModified property"""
        return self.properties.get("HasUserRecentlyModified", None)

    @odata(name="Id", beta=True)
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="IsWebWelcomePage", beta=True)
    @property
    def is_web_welcome_page(self) -> Optional[bool]:
        """Gets the IsWebWelcomePage property"""
        return self.properties.get("IsWebWelcomePage", None)

    @odata(name="LikeCount", beta=True)
    @property
    def like_count(self) -> Optional[int]:
        """Gets the LikeCount property"""
        return self.properties.get("LikeCount", None)

    @odata(name="ListId", beta=True)
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="Modified", beta=True)
    @property
    def modified(self) -> Optional[datetime.datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.datetime.min)

    @odata(name="ModifiedRelativeTime", beta=True)
    @property
    def modified_relative_time(self) -> Optional[str]:
        """Gets the ModifiedRelativeTime property"""
        return self.properties.get("ModifiedRelativeTime", None)

    @odata(name="PageLayoutType", beta=True)
    @property
    def page_layout_type(self) -> Optional[str]:
        """Gets the PageLayoutType property"""
        return self.properties.get("PageLayoutType", None)

    @odata(name="Path", beta=True)
    @property
    def path(self) -> ResourcePath:
        """Gets the Path property"""
        from office365.sharepoint.types.resource_path import ResourcePath

        return self.properties.get("Path", ResourcePath())

    @odata(name="PromotedState", beta=True)
    @property
    def promoted_state(self) -> Optional[int]:
        """Gets the PromotedState property"""
        return self.properties.get("PromotedState", None)

    @odata(name="PublishStartDate", beta=True)
    @property
    def publish_start_date(self) -> Optional[datetime.datetime]:
        """Gets the PublishStartDate property"""
        return self.properties.get("PublishStartDate", datetime.datetime.min)

    @odata(name="SocialBarOnSitePagesDisabled", beta=True)
    @property
    def social_bar_on_site_pages_disabled(self) -> Optional[bool]:
        """Gets the SocialBarOnSitePagesDisabled property"""
        return self.properties.get("SocialBarOnSitePagesDisabled", None)

    @odata(name="Title", beta=True)
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="UniqueId", beta=True)
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @odata(name="Url", beta=True)
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @odata(name="Version", beta=True)
    @property
    def version(self) -> Optional[str]:
        """Gets the Version property"""
        return self.properties.get("Version", None)
