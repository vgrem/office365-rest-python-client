from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.fields.field import Field


class FieldUrl(Field):
    """Specifies a fields that contains a URL."""

    @odata(name="DisplayFormat")
    @property
    def display_format(self) -> Optional[int]:
        """Gets the number of decimal places to be used when displaying the field."""
        return self.properties.get("DisplayFormat", None)
