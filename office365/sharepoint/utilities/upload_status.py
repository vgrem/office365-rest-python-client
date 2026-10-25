from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class UploadStatus(Entity):
    """The status of a chunk session upload."""

    @odata(name="ExpectedContentRange")
    @property
    def expected_content_range(self) -> Optional[str]:
        """The string representation of the byte offset of the stream uploaded in chunk upload session that the
        next ContinueUpload (3.2.5.64.2.1.17) call uses to continue chunk upload.
        """
        return self.properties.get("ExpectedContentRange", None)

    @odata(name="ExpirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[str]:
        """The earliest time at which the chunk upload session will be automatically expired and then deleted."""
        return self.properties.get("ExpirationDateTime", None)

    @odata(name="UploadId")
    @property
    def upload_id(self) -> Optional[str]:
        """Unique Id of the chunk session upload."""
        return self.properties.get("UploadId", None)

    @property
    def property_ref_name(self):
        return "ExpectedContentRange"

    @property
    def entity_type_name(self):
        return "SP.Utilities.UploadStatus"

    @odata(name="ExpirationDateTime")
    @property
    def expiration_datetime(self) -> Optional[datetime]:
        """Gets the ExpirationDateTime property"""
        return self.properties.get("ExpirationDateTime", datetime.min)
