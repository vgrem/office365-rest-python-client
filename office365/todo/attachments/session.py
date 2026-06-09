from datetime import datetime

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class AttachmentSession(Entity):
    """Represents a resource that uploads large attachments to a todoTask."""

    @property
    def content(self):
        """The content streams that are uploaded."""
        return self.properties.get("content", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_datetime(self) -> datetime:
        """The date and time in UTC when the upload session will expire.
        The complete file must be uploaded before this expiration time is reached."""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="nextExpectedRanges")
    @property
    def next_expected_ranges(self) -> StringCollection:
        """Indicates a single value {start} that represents the location in the file where the next
        upload should begin."""
        return self.properties.get("nextExpectedRanges", StringCollection())
