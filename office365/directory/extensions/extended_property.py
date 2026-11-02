from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SingleValueLegacyExtendedProperty(Entity):
    """An extended property that contains a single value."""

    @odata(name="value")
    @property
    def value(self) -> Optional[str]:
        """A property value."""
        return self.properties.get("value", None)


class MultiValueLegacyExtendedProperty(Entity):
    """An extended property that contains a collection of values."""

    @odata(name="value")
    @property
    def value(self) -> StringCollection:
        """A collection of property values."""
        return self.properties.get("value", StringCollection())
