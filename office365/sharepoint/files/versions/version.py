from datetime import datetime
from typing import IO, AnyStr, Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class FileVersion(Entity):
    """Represents a version of a File object."""

    def __str__(self):
        return self.version_label or ""

    def __repr__(self):
        return f"Is Current: {self.is_current_version}, {self.version_label}"

    def download(self, file_object: IO) -> Self:
        """Downloads the file version as a stream and save into a file."""

        def _save_file(return_type: ClientResult[AnyStr]) -> None:
            file_object.write(return_type.value)

        def _file_version_loaded():
            self.open_binary_stream().after_execute(_save_file)

        self.ensure_property("ID").after_execute(lambda _: _file_version_loaded())
        return self

    def open_binary_stream(self) -> ClientResult[bytes]:
        """Opens the file as a stream."""
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(self, "OpenBinaryStream", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def open_binary_stream_with_options(self, open_options: int) -> ClientResult[bytes]:
        """Opens the file as a stream."""
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(self, "OpenBinaryStreamWithOptions", [open_options], None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def created(self) -> Optional[datetime]:
        """Specifies the creation date and time for the file version."""
        return self.properties.get("Created", datetime.min)

    @odata(name="CreatedBy")
    @property
    def created_by(self):
        """Gets the user that created the file version."""
        from office365.sharepoint.principal.users.user import User

        return self.properties.get("CreatedBy", User(self.context, ResourcePath("CreatedBy", self.resource_path)))

    @property
    def id(self) -> Optional[int]:
        """Gets a file version identifier"""
        return int(self.properties.get("ID", -1))

    @property
    def url(self) -> Optional[str]:
        """Gets a value that specifies the relative URL of the file version based on the URL for the site or subsite."""
        return self.properties.get("Url", None)

    @property
    def version_label(self) -> Optional[str]:
        """Gets a value that specifies the implementation specific identifier of the file."""
        return self.properties.get("VersionLabel", None)

    @property
    def is_current_version(self) -> Optional[bool]:
        """Gets a value that specifies whether the file version is the current version."""
        return self.properties.get("IsCurrentVersion", None)

    @property
    def checkin_comment(self) -> Optional[str]:
        """Gets a value that specifies the check-in comment."""
        return self.properties.get("CheckInComment", None)

    @property
    def check_in_comment(self) -> Optional[str]:
        """Gets the CheckInComment property"""
        return self.properties.get("CheckInComment", None)

    @property
    def expiration_date(self) -> Optional[str]:
        """Gets the ExpirationDate property"""
        return self.properties.get("ExpirationDate", None)

    @property
    def length(self) -> Optional[int]:
        """Gets the Length property"""
        return self.properties.get("Length", None)

    @property
    def size(self) -> Optional[int]:
        """Gets the Size property"""
        return self.properties.get("Size", None)

    @property
    def snapshot_date(self) -> Optional[str]:
        """Gets the SnapshotDate property"""
        return self.properties.get("SnapshotDate", None)

    @property
    def property_ref_name(self) -> str:
        return "ID"

    def set_expiration_date(self, expiration_date: datetime) -> Self:
        """SetExpirationDate operation.

        Args:
            expiration_date (datetime): expirationDate parameter
        """
        qry = ServiceOperationQuery(self, "SetExpirationDate", None, {"expirationDate": expiration_date}, None, None)
        self.context.add_query(qry)
        return self
