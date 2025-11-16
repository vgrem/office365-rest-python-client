from __future__ import annotations

from typing import IO, TYPE_CHECKING

from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.sharepoint.attachments.attachment import Attachment
    from office365.sharepoint.files.file import File


def create_upload_file_query(file: File | Attachment, file_object: IO) -> ServiceOperationQuery:
    """Constructs upload file content query"""
    qry = ServiceOperationQuery(file, "$value")

    def _construct_request(request: RequestOptions) -> None:
        request.data = file_object.read()
        request.method = HttpMethod.Post
        request.set_header("X-HTTP-Method", "PUT")

    file.context.before_query_execute(_construct_request)
    return qry
