from datetime import datetime
from typing import Optional

from office365.onenote.entity_base_model import OnenoteEntityBaseModel
from office365.runtime.types.odata_property import odata


class OnenoteEntitySchemaObjectModel(OnenoteEntityBaseModel):
    """This is a base type for OneNote entities."""

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> Optional[datetime]:
        """
        The date and time when the page was created. The timestamp represents date and time information using
        ISO 8601 format and is always in UTC time. For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z.
        """
        return self.properties.get("createdDateTime", datetime.min)
