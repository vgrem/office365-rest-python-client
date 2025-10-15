from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class PointPublishingDocProps(Entity):

    @property
    def author(self) -> Optional[str]:
        """Gets the Author property"""
        return self.properties.get("Author", None)

    @property
    def content_type_id(self) -> Optional[str]:
        """Gets the ContentTypeId property"""
        return self.properties.get("ContentTypeId", None)

    @property
    def doc_library_url(self) -> Optional[str]:
        """Gets the DocLibraryUrl property"""
        return self.properties.get("DocLibraryUrl", None)

    @property
    def file_type(self) -> Optional[str]:
        """Gets the FileType property"""
        return self.properties.get("FileType", None)

    @property
    def modified(self) -> datetime:
        """Gets the Modified property"""
        return self.properties.get("Modified", None)

    @property
    def server_redirected_embed_url(self) -> Optional[str]:
        """Gets the ServerRedirectedEmbedUrl property"""
        return self.properties.get("ServerRedirectedEmbedUrl", None)

    @property
    def server_redirected_preview_url(self) -> Optional[str]:
        """Gets the ServerRedirectedPreviewUrl property"""
        return self.properties.get("ServerRedirectedPreviewUrl", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def site_title(self) -> Optional[str]:
        """Gets the SiteTitle property"""
        return self.properties.get("SiteTitle", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingDocProps"
