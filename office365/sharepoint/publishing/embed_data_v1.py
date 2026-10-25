from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class EmbedDataV1(Entity):
    """Represents embedded meta data of the page."""

    def url(self) -> Optional[str]:
        """The URL of the page."""
        return self.properties.get("Url", None)

    def video_id(self) -> Optional[str]:
        """If the page represents a video, the value will be video id."""
        return self.properties.get("VideoId", None)

    def web_id(self) -> Optional[str]:
        """If the page belongs to website, the value will be website id, otherwise the value will be empty."""
        return self.properties.get("WebId", None)

    @odata(name="AllowHttpsEmbed")
    @property
    def allow_https_embed(self) -> Optional[bool]:
        """Gets the AllowHttpsEmbed property"""
        return self.properties.get("AllowHttpsEmbed", None)

    @odata(name="CreatorName")
    @property
    def creator_name(self) -> Optional[str]:
        """Gets the CreatorName property"""
        return self.properties.get("CreatorName", None)

    @odata(name="DatePublishedAt")
    @property
    def date_published_at(self) -> Optional[str]:
        """Gets the DatePublishedAt property"""
        return self.properties.get("DatePublishedAt", None)

    @odata(name="DecodedUrl")
    @property
    def decoded_url(self) -> Optional[str]:
        """Gets the DecodedUrl property"""
        return self.properties.get("DecodedUrl", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="DurationInSeconds")
    @property
    def duration_in_seconds(self) -> Optional[int]:
        """Gets the DurationInSeconds property"""
        return self.properties.get("DurationInSeconds", None)

    @odata(name="EmbedServiceResponseCode")
    @property
    def embed_service_response_code(self) -> Optional[int]:
        """Gets the EmbedServiceResponseCode property"""
        return self.properties.get("EmbedServiceResponseCode", None)

    @odata(name="ErrorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="Html")
    @property
    def html(self) -> Optional[str]:
        """Gets the Html property"""
        return self.properties.get("Html", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[str]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="PublisherName")
    @property
    def publisher_name(self) -> Optional[str]:
        """Gets the PublisherName property"""
        return self.properties.get("PublisherName", None)

    @odata(name="ResponseCode")
    @property
    def response_code(self) -> Optional[int]:
        """Gets the ResponseCode property"""
        return self.properties.get("ResponseCode", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[str]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

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

    @odata(name="Type")
    @property
    def type_(self) -> Optional[str]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[str]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.EmbedDataV1"

    @odata(name="Type")
    @property
    def type(self) -> Optional[str]:
        """Gets the Type property"""
        return self.properties.get("Type", None)
