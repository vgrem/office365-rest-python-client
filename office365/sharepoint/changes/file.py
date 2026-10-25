from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change


class ChangeFile(Change):
    """Specifies a change on a file not contained in a document library."""

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[str]:
        """Identifies the file that changed."""
        return self.properties.get("UniqueId", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[str]:
        """Identifies the site that contains the changed file."""
        return self.properties.get("WebId", None)
