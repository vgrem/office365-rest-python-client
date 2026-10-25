from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class VideoServiceDiscoverer(Entity):
    def __init__(self, context):
        super().__init__(context, ResourcePath("SP.Publishing.VideoServiceDiscoverer"))

    @odata(name="VideoPortalUrl")
    @property
    def video_portal_url(self) -> Optional[str]:
        """ """
        return self.properties.get("VideoPortalUrl", None)

    @odata(name="ChannelUrlTemplate")
    @property
    def channel_url_template(self) -> Optional[str]:
        """Gets the ChannelUrlTemplate property"""
        return self.properties.get("ChannelUrlTemplate", None)

    @odata(name="IsFeedbackEnabled")
    @property
    def is_feedback_enabled(self) -> Optional[bool]:
        """Gets the IsFeedbackEnabled property"""
        return self.properties.get("IsFeedbackEnabled", None)

    @odata(name="IsLicensedForVideoPortal")
    @property
    def is_licensed_for_video_portal(self) -> Optional[bool]:
        """Gets the IsLicensedForVideoPortal property"""
        return self.properties.get("IsLicensedForVideoPortal", None)

    @odata(name="IsMigratedToStream")
    @property
    def is_migrated_to_stream(self) -> Optional[bool]:
        """Gets the IsMigratedToStream property"""
        return self.properties.get("IsMigratedToStream", None)

    @odata(name="IsO365VideoEnabled")
    @property
    def is_o365_video_enabled(self) -> Optional[bool]:
        """Gets the IsO365VideoEnabled property"""
        return self.properties.get("IsO365VideoEnabled", None)

    @odata(name="IsVideoPortalEnabled")
    @property
    def is_video_portal_enabled(self) -> Optional[bool]:
        """Gets the IsVideoPortalEnabled property"""
        return self.properties.get("IsVideoPortalEnabled", None)

    @odata(name="O365VideoPageUrl")
    @property
    def o365_video_page_url(self) -> Optional[str]:
        """Gets the O365VideoPageUrl property"""
        return self.properties.get("O365VideoPageUrl", None)

    @odata(name="PlayerUrlTemplate")
    @property
    def player_url_template(self) -> Optional[str]:
        """Gets the PlayerUrlTemplate property"""
        return self.properties.get("PlayerUrlTemplate", None)

    @odata(name="VideoPortalLayoutsUrl")
    @property
    def video_portal_layouts_url(self) -> Optional[str]:
        """Gets the VideoPortalLayoutsUrl property"""
        return self.properties.get("VideoPortalLayoutsUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoServiceDiscoverer"
