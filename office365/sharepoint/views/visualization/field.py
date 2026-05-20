from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VisualizationField(ClientValue):
    """Contains CSS properties relating to how an individual field is layed out relative to it's container.

    internal_name: A Property which will specify which set of sub-elements to apply this set of
        CSS properties on.
    style: CSS properties in serialized JSON format.
    """

    InternalName: Optional[str] = None
    Style: Optional[str] = None
