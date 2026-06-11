from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.customizedformspage import CustomizedFormsPage


@dataclass
class CustomizedFormsPageCollection(ClientValue):
    Items: ClientValueCollection[CustomizedFormsPage] = field(
        default_factory=lambda: ClientValueCollection(CustomizedFormsPage)
    )
