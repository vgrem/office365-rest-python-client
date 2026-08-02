from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.onedrive.driveitems.publication_facet import PublicationFacet
from office365.runtime.types.odata_property import odata


class BaseItemVersion(Entity):
    """Represents a previous version of an item or entity."""

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Identity of the user which last modified the version. Read-only."""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_datetime(self) -> datetime:
        """Gets date and time the item was last modified."""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def publication(self) -> PublicationFacet:
        """Indicates the publication status of this particular version. Read-only."""
        return self.properties.get("publication", PublicationFacet())
