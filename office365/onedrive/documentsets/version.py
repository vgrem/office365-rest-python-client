from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.directory.permissions.identity_set import IdentitySet
from office365.onedrive.documentsets.version_item import DocumentSetVersionItem
from office365.onedrive.versions.list_item import ListItemVersion
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class DocumentSetVersion(ListItemVersion):
    """Represents the version of a document set item in a list."""

    @odata(name="comment")
    @property
    def comment(self) -> Optional[str]:
        """Comment about the captured version."""
        return self.properties.get("comment", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """User who captured the version."""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """Date and time when this version was created."""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="items")
    @property
    def items(self) -> ClientValueCollection[DocumentSetVersionItem]:
        """Items within the document set that are captured as part of this version."""
        return self.properties.get("items", ClientValueCollection(DocumentSetVersionItem))

    @odata(name="shouldCaptureMinorVersion")
    @property
    def should_capture_minor_version(self) -> Optional[bool]:
        """
        If true, minor versions of items are also captured; otherwise, only major versions will be captured.
        Default value is false.
        """
        return self.properties.get("shouldCaptureMinorVersion", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DocumentSetVersion"

    @require_permission(
        delegated=["Sites.ReadWrite.All", "Sites.FullControl.All", "Sites.Manage.All", "Sites.Selected"],
        application=["Sites.ReadWrite.All", "Sites.FullControl.All", "Sites.Manage.All", "Sites.Selected"],
    )
    def restore(self) -> Self:
        """restore operation."""
        qry = ServiceOperationQuery(self, "restore", None, {}, None, None)
        self.context.add_query(qry)
        return self
