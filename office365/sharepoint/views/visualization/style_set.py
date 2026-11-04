from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.views.visualization.field import VisualizationField


@value
class VisualizationStyleSet(ClientValue):
    """Microsoft.SharePoint.Client.VisualizationStyleSet is not applicable."""

    AspectRatio: Optional[str] = None
    BackgroundColor: Optional[str] = None
    Fields: ClientValueCollection[VisualizationField] = field(
        default_factory=lambda: ClientValueCollection(VisualizationField)
    )
    MinHeight: Optional[str] = None
