from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change


class ChangeView(Change):
    """Specifies a change on a view."""

    @odata(name="ViewId")
    @property
    def view_id(self) -> Optional[str]:
        """Identifies the changed view."""
        return self.properties.get("ViewId", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[str]:
        """Identifies the list that contains the changed view."""
        return self.properties.get("ListId", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[str]:
        """Identifies the site that contains the changed view."""
        return self.properties.get("WebId", None)
