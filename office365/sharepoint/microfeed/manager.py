from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.entity import Entity


class MicrofeedManager(Entity):
    def __init__(self, context):
        super().__init__(context, StaticPath("SP.Microfeed.MicrofeedManager"))
