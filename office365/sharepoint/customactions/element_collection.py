from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.customactions.element import CustomActionElement


class CustomActionElementCollection(ClientValue):
    """This is the class that represents a collection of CustomActionElement."""

    Items: ClientValueCollection[CustomActionElement] = field(
        default_factory=lambda: ClientValueCollection(CustomActionElement)
    )
