from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.portal.userprofiles.sharedwithme.document_user import (
    SharedWithMeDocumentUser,
)


class SharedWithMeDocument(Entity):
    """Represents a shared document."""

    @odata(name="Authors")
    @property
    def authors(self) -> ClientValueCollection[SharedWithMeDocumentUser]:
        """Specifies a list of users that authored the document."""
        return self.properties.get("Authors", ClientValueCollection(SharedWithMeDocumentUser))

    @odata(name="CallerStack")
    @property
    def caller_stack(self) -> Optional[str]:
        """ """
        return self.properties.get("CallerStack", None)

    @odata(name="ContentTypeId")
    @property
    def content_type_id(self) -> Optional[str]:
        """Specifies the identifier of the content type of the document."""
        return self.properties.get("ContentTypeId", None)

    @odata(name="DocId")
    @property
    def doc_id(self) -> Optional[str]:
        """Specifies the document identifier."""
        return self.properties.get("DocId", None)

    @odata(name="Editors")
    @property
    def editors(self) -> ClientValueCollection[SharedWithMeDocumentUser]:
        """Specifies a list of users that can edit the document."""
        return self.properties.get("Editors", ClientValueCollection(SharedWithMeDocumentUser))

    @odata(name="Modified")
    @property
    def modified(self) -> datetime:
        """Specifies the date and time when the document was last modified."""
        return self.properties.get("Modified", datetime.min)

    @odata(name="FileLeafRef")
    @property
    def file_leaf_ref(self) -> Optional[str]:
        """Specifies the name of the document."""
        return self.properties.get("FileLeafRef", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.UserProfiles.SharedWithMeDocument"

    @odata(name="ChildCount")
    @property
    def child_count(self) -> Optional[int]:
        """Gets the ChildCount property"""
        return self.properties.get("ChildCount", None)

    @odata(name="ClickThroughId")
    @property
    def click_through_id(self) -> Optional[str]:
        """Gets the ClickThroughId property"""
        return self.properties.get("ClickThroughId", None)

    @odata(name="ColorIndex")
    @property
    def color_index(self) -> Optional[str]:
        """Gets the ColorIndex property"""
        return self.properties.get("ColorIndex", None)

    @odata(name="CommentCount")
    @property
    def comment_count(self) -> Optional[int]:
        """Gets the CommentCount property"""
        return self.properties.get("CommentCount", None)

    @odata(name="CoverPhotoId")
    @property
    def cover_photo_id(self) -> Optional[str]:
        """Gets the CoverPhotoId property"""
        return self.properties.get("CoverPhotoId", None)

    @odata(name="CreatedDateTime")
    @property
    def created_datetime(self) -> Optional[datetime]:
        """Gets the CreatedDateTime property"""
        return self.properties.get("CreatedDateTime", datetime.min)

    @odata(name="CreatedDateTimeUTC")
    @property
    def created_datetime_utc(self) -> Optional[datetime]:
        """Gets the CreatedDateTimeUTC property"""
        return self.properties.get("CreatedDateTimeUTC", datetime.min)

    @odata(name="Extension")
    @property
    def extension(self) -> Optional[str]:
        """Gets the Extension property"""
        return self.properties.get("Extension", None)

    @odata(name="FileRef")
    @property
    def file_ref(self) -> Optional[str]:
        """Gets the FileRef property"""
        return self.properties.get("FileRef", None)

    @odata(name="Id")
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="IsContainer")
    @property
    def is_container(self) -> Optional[bool]:
        """Gets the IsContainer property"""
        return self.properties.get("IsContainer", None)

    @odata(name="IsMyDocument")
    @property
    def is_my_document(self) -> Optional[bool]:
        """Gets the IsMyDocument property"""
        return self.properties.get("IsMyDocument", None)

    @odata(name="ItemDescription")
    @property
    def item_description(self) -> Optional[str]:
        """Gets the ItemDescription property"""
        return self.properties.get("ItemDescription", None)

    @odata(name="ItemResourceId")
    @property
    def item_resource_id(self) -> Optional[str]:
        """Gets the ItemResourceId property"""
        return self.properties.get("ItemResourceId", None)

    @odata(name="ItemSize")
    @property
    def item_size(self) -> Optional[float]:
        """Gets the ItemSize property"""
        return self.properties.get("ItemSize", None)

    @odata(name="LinkingUrl")
    @property
    def linking_url(self) -> Optional[str]:
        """Gets the LinkingUrl property"""
        return self.properties.get("LinkingUrl", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[str]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="ListItemId")
    @property
    def list_item_id(self) -> Optional[str]:
        """Gets the ListItemId property"""
        return self.properties.get("ListItemId", None)

    @odata(name="LocalItemUniqueId")
    @property
    def local_item_unique_id(self) -> Optional[str]:
        """Gets the LocalItemUniqueId property"""
        return self.properties.get("LocalItemUniqueId", None)

    @odata(name="LocalItemUniqueIdCollection")
    @property
    def local_item_unique_id_collection(self) -> Optional[str]:
        """Gets the LocalItemUniqueIdCollection property"""
        return self.properties.get("LocalItemUniqueIdCollection", None)

    @odata(name="MediaBaseUrl")
    @property
    def media_base_url(self) -> Optional[str]:
        """Gets the MediaBaseUrl property"""
        return self.properties.get("MediaBaseUrl", None)

    @odata(name="ModifiedDateTimeUTC")
    @property
    def modified_datetime_utc(self) -> Optional[datetime]:
        """Gets the ModifiedDateTimeUTC property"""
        return self.properties.get("ModifiedDateTimeUTC", datetime.min)

    @odata(name="OfficeBundleGenerate")
    @property
    def office_bundle_generate(self) -> Optional[str]:
        """Gets the OfficeBundleGenerate property"""
        return self.properties.get("OfficeBundleGenerate", None)

    @odata(name="OfficeBundleGetFragment")
    @property
    def office_bundle_get_fragment(self) -> Optional[str]:
        """Gets the OfficeBundleGetFragment property"""
        return self.properties.get("OfficeBundleGetFragment", None)

    @odata(name="Owner")
    @property
    def owner(self) -> SharedWithMeDocumentUser:
        """Gets the Owner property"""
        from office365.sharepoint.portal.userprofiles.sharedwithme.document_user import (
            SharedWithMeDocumentUser,
        )

        return self.properties.get("Owner", SharedWithMeDocumentUser())

    @odata(name="ParentId")
    @property
    def parent_id(self) -> Optional[str]:
        """Gets the ParentId property"""
        return self.properties.get("ParentId", None)

    @odata(name="ParentLink")
    @property
    def parent_link(self) -> Optional[str]:
        """Gets the ParentLink property"""
        return self.properties.get("ParentLink", None)

    @odata(name="PdfConversionUrl")
    @property
    def pdf_conversion_url(self) -> Optional[str]:
        """Gets the PdfConversionUrl property"""
        return self.properties.get("PdfConversionUrl", None)

    @odata(name="ProgId")
    @property
    def prog_id(self) -> Optional[str]:
        """Gets the ProgId property"""
        return self.properties.get("ProgId", None)

    @odata(name="RemoteItemPermMask")
    @property
    def remote_item_perm_mask(self) -> Optional[int]:
        """Gets the RemoteItemPermMask property"""
        return self.properties.get("RemoteItemPermMask", None)

    @odata(name="ServerRedirectedEmbedUrl")
    @property
    def server_redirected_embed_url(self) -> Optional[str]:
        """Gets the ServerRedirectedEmbedUrl property"""
        return self.properties.get("ServerRedirectedEmbedUrl", None)

    @odata(name="ServerRedirectedPreviewUrl")
    @property
    def server_redirected_preview_url(self) -> Optional[str]:
        """Gets the ServerRedirectedPreviewUrl property"""
        return self.properties.get("ServerRedirectedPreviewUrl", None)

    @odata(name="ServerRedirectedUrl")
    @property
    def server_redirected_url(self) -> Optional[str]:
        """Gets the ServerRedirectedUrl property"""
        return self.properties.get("ServerRedirectedUrl", None)

    @odata(name="SharedDateTimeUTC")
    @property
    def shared_datetime_utc(self) -> Optional[datetime]:
        """Gets the SharedDateTimeUTC property"""
        return self.properties.get("SharedDateTimeUTC", datetime.min)

    @odata(name="SharedToGroupGroupDisplayName")
    @property
    def shared_to_group_group_display_name(self) -> Optional[str]:
        """Gets the SharedToGroupGroupDisplayName property"""
        return self.properties.get("SharedToGroupGroupDisplayName", None)

    @odata(name="SharedToGroupGroupId")
    @property
    def shared_to_group_group_id(self) -> Optional[str]:
        """Gets the SharedToGroupGroupId property"""
        return self.properties.get("SharedToGroupGroupId", None)

    @odata(name="SharedWithInternal")
    @property
    def shared_with_internal(self) -> ClientValueCollection[SharedWithMeDocumentUser]:
        """Gets the SharedWithInternal property"""
        from office365.sharepoint.portal.userprofiles.sharedwithme.document_user import (
            SharedWithMeDocumentUser,
        )

        return self.properties.get(
            "SharedWithInternal", ClientValueCollection[SharedWithMeDocumentUser](SharedWithMeDocumentUser)
        )

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[str]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="SiteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @odata(name="SpResourceUrl")
    @property
    def sp_resource_url(self) -> Optional[str]:
        """Gets the SpResourceUrl property"""
        return self.properties.get("SpResourceUrl", None)

    @odata(name="SWMSourceFlag")
    @property
    def swm_source_flag(self) -> Optional[int]:
        """Gets the SWMSourceFlag property"""
        return self.properties.get("SWMSourceFlag", None)

    @odata(name="TenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the TenantId property"""
        return self.properties.get("TenantId", None)

    @odata(name="TenantName")
    @property
    def tenant_name(self) -> Optional[str]:
        """Gets the TenantName property"""
        return self.properties.get("TenantName", None)

    @odata(name="ThumbnailUrl")
    @property
    def thumbnail_url(self) -> Optional[str]:
        """Gets the ThumbnailUrl property"""
        return self.properties.get("ThumbnailUrl", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[str]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @odata(name="UrlPath")
    @property
    def url_path(self) -> Optional[str]:
        """Gets the UrlPath property"""
        return self.properties.get("UrlPath", None)

    @odata(name="VideoManifestUrl")
    @property
    def video_manifest_url(self) -> Optional[str]:
        """Gets the VideoManifestUrl property"""
        return self.properties.get("VideoManifestUrl", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[str]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @odata(name="WebTemplateId")
    @property
    def web_template_id(self) -> Optional[int]:
        """Gets the WebTemplateId property"""
        return self.properties.get("WebTemplateId", None)

    @odata(name="WebUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the WebUrl property"""
        return self.properties.get("WebUrl", None)
