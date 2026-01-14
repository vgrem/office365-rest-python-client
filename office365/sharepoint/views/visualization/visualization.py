from office365.runtime.client_value import ClientValue
from office365.sharepoint.views.visualization.style_set import VisualizationStyleSet
from office365.sharepoint.viva.visualizationappinfo import VisualizationAppInfo


class Visualization(ClientValue):
    def __init__(
        self,
        default_screen: VisualizationStyleSet = VisualizationStyleSet(),
        detail_view: VisualizationStyleSet = VisualizationStyleSet(),
        medium_screen: VisualizationStyleSet = VisualizationStyleSet(),
        small_screen: VisualizationStyleSet = VisualizationStyleSet(),
        visualization_app_info: VisualizationAppInfo = VisualizationAppInfo(),
        visualization_type: int = None,
    ):
        """ """
        self.DefaultScreen = default_screen
        self.DetailView = detail_view
        self.MediumScreen = medium_screen
        self.SmallScreen = small_screen
        self.VisualizationAppInfo = visualization_app_info
        self.VisualizationType = visualization_type
