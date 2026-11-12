from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.print.document_upload_properties import PrintDocumentUploadProperties
    from office365.runtime.odata.v4.upload_session import UploadSession


class PrintDocument(Entity):
    @odata(name="contentType")
    @property
    def content_type(self) -> Optional[str]:
        """Gets the contentType property"""
        return self.properties.get("contentType", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="downloadedDateTime")
    @property
    def downloaded_date_time(self) -> Optional[datetime]:
        """Gets the downloadedDateTime property"""
        return self.properties.get("downloadedDateTime", datetime.min)

    @odata(name="size")
    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @odata(name="uploadedDateTime")
    @property
    def uploaded_date_time(self) -> Optional[datetime]:
        """Gets the uploadedDateTime property"""
        return self.properties.get("uploadedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintDocument"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["PrintJob.Create", "PrintJob.ReadWrite", "PrintJob.ReadWrite.All"],
        application=["PrintJob.ReadWrite.All"],
    )
    def create_upload_session(self, properties: PrintDocumentUploadProperties) -> ClientResult[UploadSession]:
        """createUploadSession operation.

        Args:
            properties (PrintDocumentUploadProperties):
                properties parameter
        """
        from office365.runtime.odata.v4.upload_session import UploadSession

        return_type = ClientResult(self.context, UploadSession())
        qry = ServiceOperationQuery(self, "createUploadSession", None, {"properties": properties}, None, return_type)
        self.context.add_query(qry)
        return return_type
