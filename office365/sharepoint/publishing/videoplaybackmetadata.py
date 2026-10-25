from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class VideoPlaybackMetadata(Entity):
    @odata(name="HLSUrl")
    @property
    def hls_url(self) -> Optional[str]:
        """Gets the HLSUrl property"""
        return self.properties.get("HLSUrl", None)

    @odata(name="SdnPlaybackMetadata")
    @property
    def sdn_playback_metadata(self) -> Optional[str]:
        """Gets the SdnPlaybackMetadata property"""
        return self.properties.get("SdnPlaybackMetadata", None)

    @odata(name="StreamingUrl")
    @property
    def streaming_url(self) -> Optional[str]:
        """Gets the StreamingUrl property"""
        return self.properties.get("StreamingUrl", None)

    @odata(name="Token")
    @property
    def token(self) -> Optional[str]:
        """Gets the Token property"""
        return self.properties.get("Token", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoPlaybackMetadata"
