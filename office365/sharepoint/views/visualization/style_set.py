from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.views.visualization.field import VisualizationField


class VisualizationStyleSet(ClientValue):
    def __init__(
        self,
        aspect_ratio: str = None,
        background_color: str = None,
        fields: ClientValueCollection[VisualizationField] = ClientValueCollection(VisualizationField),
        min_height: str = None,
    ):
        """Microsoft.SharePoint.Client.VisualizationStyleSet is not applicable."""
        self.AspectRatio = aspect_ratio
        self.BackgroundColor = background_color
        self.Fields = fields
        self.MinHeight = min_height
