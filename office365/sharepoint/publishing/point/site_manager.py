from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity


class PointPublishingSiteManager(Entity):
    """"""

    def __init__(self, context):
        super().__init__(
            context, ResourcePath("SP.Publishing.PointPublishingSiteManager")
        )
