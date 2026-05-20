from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.views.visualization.style_set import VisualizationStyleSet
from office365.sharepoint.viva.visualizationappinfo import VisualizationAppInfo


@dataclass
class Visualization(ClientValue):
    DefaultScreen: VisualizationStyleSet = field(default_factory=VisualizationStyleSet)
    DetailView: VisualizationStyleSet = field(default_factory=VisualizationStyleSet)
    MediumScreen: VisualizationStyleSet = field(default_factory=VisualizationStyleSet)
    SmallScreen: VisualizationStyleSet = field(default_factory=VisualizationStyleSet)
    VisualizationAppInfo: "VisualizationAppInfo" = field(default_factory=VisualizationAppInfo)
    VisualizationType: Optional[int] = None
