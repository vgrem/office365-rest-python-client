from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ImageFieldValue(ClientValue):
    """
    Fields:
        serverRelativeUrl (str | None):
    """

    serverRelativeUrl: str | None = None
    type: tuple = ("thumbnail",)
    fileName: str | None = None
    nativeFile: dict = field(default_factory=dict)
    fieldName: str = "Image"
    serverUrl: str | None = None
    fieldId: str | None = None
    id: str | None = None

    @property
    def entity_type_name(self):
        return None
