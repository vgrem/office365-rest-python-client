from datetime import datetime
from typing import Any

from typing_extensions import Self

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.onedrive.driveitems.publication_facet import PublicationFacet


class BaseItemVersion(Entity):
    """Represents a previous version of an item or entity."""

    @property
    def last_modified_by(self) -> IdentitySet:
        """Identity of the user which last modified the version. Read-only."""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @property
    def last_modified_datetime(self) -> datetime:
        """Gets date and time the item was last modified."""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def publication(self) -> PublicationFacet:
        """Indicates the publication status of this particular version. Read-only."""
        return self.properties.get("publication", PublicationFacet())

    def get_property(self, name: str, default_value: Any = None) -> Self:
        if default_value is None:
            property_mapping = {
                "lastModifiedBy": self.last_modified_by,
                "lastModifiedDateTime": self.last_modified_datetime,
            }
            default_value = property_mapping.get(name, None)
        return super(BaseItemVersion, self).get_property(name, default_value)
