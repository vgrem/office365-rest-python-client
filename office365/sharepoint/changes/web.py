from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change


class ChangeWeb(Change):
    """Specifies a change on a site"""

    def __repr__(self):
        return f"Web: {self.web_id}, Action: {self.change_type_name}"

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[str]:
        """
        Identifies the site that has changed
        """
        return self.properties.get("WebId", None)
