from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PointPublishingDocProps(Entity):
    @odata(name="Author")
    @property
    def author(self) -> Optional[str]:
        """Gets the Author property"""
        return self.properties.get("Author", None)

    @odata(name="ContentTypeId")
    @property
    def content_type_id(self) -> Optional[str]:
        """Gets the ContentTypeId property"""
        return self.properties.get("ContentTypeId", None)

    @odata(name="DocLibraryUrl")
    @property
    def doc_library_url(self) -> Optional[str]:
        """Gets the DocLibraryUrl property"""
        return self.properties.get("DocLibraryUrl", None)

    @odata(name="FileType")
    @property
    def file_type(self) -> Optional[str]:
        """Gets the FileType property"""
        return self.properties.get("FileType", None)

    @odata(name="Modified")
    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", None)

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

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="SiteTitle")
    @property
    def site_title(self) -> Optional[str]:
        """Gets the SiteTitle property"""
        return self.properties.get("SiteTitle", None)

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

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingDocProps"
