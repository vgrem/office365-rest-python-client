from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.contenttypes.content_type_id import ContentTypeId
from office365.sharepoint.entity import Entity
from office365.sharepoint.sharing.principal import Principal


class SharedDocumentInfo(Entity):
    """"""

    @odata(name="Activity")
    @property
    def activity(self) -> Optional[str]:
        """"""
        return self.properties.get("Activity", None)

    @odata(name="Author")
    @property
    def author(self):
        """"""
        return self.properties.get("Author", Principal())

    @odata(name="CallerStack")
    @property
    def caller_stack(self) -> Optional[str]:
        """"""
        return self.properties.get("CallerStack", None)

    @odata(name="ColorHex")
    @property
    def color_hex(self) -> Optional[str]:
        """"""
        return self.properties.get("ColorHex", None)

    @odata(name="ColorTag")
    @property
    def color_tag(self) -> Optional[str]:
        """"""
        return self.properties.get("ColorTag", None)

    @odata(name="ContentTypeId")
    @property
    def content_type_id(self) -> Optional[str]:
        """"""
        return self.properties.get("ContentTypeId", ContentTypeId())

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharedDocumentInfo"

    @odata(name="DriveAccessToken")
    @property
    def drive_access_token(self) -> Optional[str]:
        """Gets the DriveAccessToken property"""
        return self.properties.get("DriveAccessToken", None)

    @odata(name="DriveAccessTokenV21")
    @property
    def drive_access_token_v21(self) -> Optional[str]:
        """Gets the DriveAccessTokenV21 property"""
        return self.properties.get("DriveAccessTokenV21", None)

    @odata(name="DriveUrl")
    @property
    def drive_url(self) -> Optional[str]:
        """Gets the DriveUrl property"""
        return self.properties.get("DriveUrl", None)

    @odata(name="Editor")
    @property
    def editor(self) -> Principal:
        """Gets the Editor property"""
        from office365.sharepoint.sharing.principal import Principal

        return self.properties.get("Editor", Principal())

    @odata(name="Emoji")
    @property
    def emoji(self) -> Optional[str]:
        """Gets the Emoji property"""
        return self.properties.get("Emoji", None)

    @odata(name="Extension")
    @property
    def extension(self) -> Optional[str]:
        """Gets the Extension property"""
        return self.properties.get("Extension", None)

    @odata(name="FileLeafRef")
    @property
    def file_leaf_ref(self) -> Optional[str]:
        """Gets the FileLeafRef property"""
        return self.properties.get("FileLeafRef", None)

    @odata(name="FileRef")
    @property
    def file_ref(self) -> Optional[str]:
        """Gets the FileRef property"""
        return self.properties.get("FileRef", None)

    @odata(name="IsContainer")
    @property
    def is_container(self) -> Optional[bool]:
        """Gets the IsContainer property"""
        return self.properties.get("IsContainer", None)

    @odata(name="LinkingUrl")
    @property
    def linking_url(self) -> Optional[str]:
        """Gets the LinkingUrl property"""
        return self.properties.get("LinkingUrl", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="ListItemId")
    @property
    def list_item_id(self) -> Optional[int]:
        """Gets the ListItemId property"""
        return self.properties.get("ListItemId", None)

    @odata(name="MediaBaseUrl")
    @property
    def media_base_url(self) -> Optional[str]:
        """Gets the MediaBaseUrl property"""
        return self.properties.get("MediaBaseUrl", None)

    @odata(name="Modified")
    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

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

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="SiteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @odata(name="SpItemUrl")
    @property
    def sp_item_url(self) -> Optional[str]:
        """Gets the SpItemUrl property"""
        return self.properties.get("SpItemUrl", None)

    @odata(name="SpResourceUrl")
    @property
    def sp_resource_url(self) -> Optional[str]:
        """Gets the SpResourceUrl property"""
        return self.properties.get("SpResourceUrl", None)

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
    def unique_id(self) -> Optional[UUID]:
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
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)
