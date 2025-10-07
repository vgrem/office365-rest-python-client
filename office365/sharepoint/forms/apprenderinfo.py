from office365.runtime.client_value import ClientValue


class AppRenderInfo(ClientValue):

    def __init__(
        self,
        background_color: str = None,
        primary_device_height: str = None,
        primary_device_width: str = None,
    ):
        self.BackgroundColor = background_color
        self.PrimaryDeviceHeight = primary_device_height
        self.PrimaryDeviceWidth = primary_device_width

    @property
    def entity_type_name(self):
        return "SP.Internal.AppRenderInfo"
