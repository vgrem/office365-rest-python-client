from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Callable, Optional

import requests

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.outlook.mail.attachments.attachment import Attachment
from office365.outlook.mail.attachments.attachment_item import AttachmentItem
from office365.runtime.client_result import ClientResult
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.v4.upload_session import UploadSession
from office365.runtime.odata.v4.upload_session_request import UploadSessionRequest
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.upload_session import UploadSessionQuery
from office365.runtime.utilities import parse_query_param

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class AttachmentCollection(EntityCollection[Attachment]):
    """Attachment collection"""

    def __init__(self, context: GraphClient, resource_path: Optional[ResourcePath] = None) -> None:
        super().__init__(context, Attachment, resource_path)

    @require_permission(delegated=["Mail.ReadWrite"], application=["Mail.ReadWrite"])
    def add_file(
        self,
        name: str,
        content: bytes | str | None = None,
        content_type: str | None = None,
        base64_content: bytes | None = None,
    ):
        """Attach a file to message

        Args:
            name (str): The name representing the text that is displayed below the icon representing the embedded attachment
            content (str or None): The contents of the file
            content_type (str or None): The content type of the attachment.
            base64_content (str or None): The contents of the file in the form of a base64 string.
        """
        if not content and not base64_content:
            raise TypeError("Either content or base64_content is required")
        from office365.outlook.mail.attachments.file import FileAttachment

        return_type = FileAttachment(self.context)
        return_type.name = name
        if base64_content:
            content_bytes: bytes = base64_content
        else:
            assert content is not None
            content_str = content if isinstance(content, str) else content.decode("utf-8")
            content_bytes = base64.b64encode(content_str.encode("utf-8"))
        return_type.content_bytes = content_bytes
        if content_type:
            return_type.content_type = content_type
        self.add_child(return_type)
        return self

    def resumable_upload(
        self,
        source_path: str,
        chunk_size: int = 1000000,
        chunk_uploaded: Callable[[int], None] | None = None,
    ):
        """Create an upload session to allow your app to upload files up to the maximum file size.
        An upload session allows your app to upload ranges of the file in sequential API requests,
        which allows the transfer to be resumed if a connection is dropped while the upload is in progress.

        Args:
            source_path (str): Local file path
            chunk_size (int): File chunk size
            chunk_uploaded ((int)->None): Upload action
        """
        from office365.outlook.mail.attachments.attachment_item import AttachmentItem
        from office365.outlook.mail.attachments.file import FileAttachment

        return_type = FileAttachment(self.context)
        self.add_child(return_type)

        qry = UploadSessionQuery(self, {"AttachmentItem": AttachmentItem.create_file(source_path)})

        def _start_upload(result: ClientResult[UploadSession]) -> None:
            with open(source_path, "rb") as local_file:
                session_request = UploadSessionRequest(local_file, chunk_size, chunk_uploaded)

                def _construct_request(request: RequestOptions) -> None:
                    auth_token = parse_query_param(request.url, "authtoken")
                    request.set_header("Authorization", f"Bearer {auth_token}")

                def _process_response(response: requests.Response) -> None:
                    location = response.headers.get("Location", None)
                    if location is None:
                        return
                    attachment_id = location[location.find("Attachments(") + 13 : -2]
                    return_type.set_property("id", attachment_id)

                session_request.beforeExecute += _construct_request
                session_request.afterExecute += _process_response
                session_request.execute_query(qry)

        self.context.add_query(qry).after_execute(_start_upload, execute_first=True)
        return self

    @require_permission(
        delegated=["Mail.ReadWrite"],
        application=["Mail.ReadWrite"],
        notes="Create an upload session for attaching a large file",
    )
    def create_upload_session(self, attachment_item: AttachmentItem) -> ClientResult[UploadSession]:
        """Create an upload session that allows an app to iteratively upload ranges of a file,
        so as to attach the file to the specified Outlook item. The item can be a message or event.

        Args:
            attachment_item (office365.mail.attachment_item.AttachmentItem):
        """
        qry = UploadSessionQuery(self, {"AttachmentItem": attachment_item})
        self.context.add_query(qry)
        return qry.return_type
