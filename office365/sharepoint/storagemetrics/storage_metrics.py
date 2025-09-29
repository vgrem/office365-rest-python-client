from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class StorageMetrics(Entity):
    """Specifies the storage-related metrics for list folders in the site"""

    @property
    def additional_file_stream_size(self) -> Optional[int]:
        """ """
        return self.properties.get("AdditionalFileStreamSize", None)

    @property
    def last_modified(self) -> Optional[datetime]:
        """
        Last modified date for all the items under the corresponding folder.
        """
        return self.properties.get("LastModified", datetime.min)

    @property
    def total_file_count(self) -> Optional[int]:
        """
        Aggregate number of files within the corresponding folder and its sub-folders.
        Excludes versions, list item attachments, and non-customized documents.
        """
        return self.properties.get("TotalFileCount", None)

    @property
    def total_file_stream_size(self) -> Optional[int]:
        """
        Aggregate stream size in bytes for all files under the corresponding folder and its sub-folders.
        Excludes version, metadata, list item attachment, and non-customized document sizes.
        """
        return self.properties.get("TotalFileStreamSize", None)

    @property
    def total_size(self) -> Optional[int]:
        """
        Aggregate of total sizes in bytes for all items under the corresponding folder and its sub-folders.
        Total size for a file/folder includes stream, version, and metadata sizes.
        """
        return self.properties.get("TotalSize", None)

    @property
    def version_count(self) -> Optional[int]:
        """ """
        return self.properties.get("VersionCount", None)

    @property
    def version_size(self) -> Optional[int]:
        """ """
        return self.properties.get("VersionSize", None)
