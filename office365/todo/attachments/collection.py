from __future__ import annotations

import base64
from typing import Optional, Union

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.todo.attachments.base import AttachmentBase
from office365.todo.attachments.info import AttachmentInfo
from office365.todo.attachments.session import AttachmentSession
from office365.todo.attachments.task_file import TaskFileAttachment
from office365.todo.attachments.type import AttachmentType


class AttachmentBaseCollection(EntityCollection[AttachmentBase]):
    """Attachment's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, AttachmentBase, resource_path)

    @require_permission(delegated=["Tasks.ReadWrite"])
    def add(
        self,
        name: str,
        content: Union[bytes, bytearray, str],
        content_type: Optional[str] = None,
        size: Optional[int] = None,
    ) -> TaskFileAttachment:
        """Add a file attachment (up to 3 MB) to a task.

        Args:
            name (str): Display name of the attachment.
            content (bytes or str): Raw bytes (base64-encoded automatically) or an
              already base64-encoded string.
            content_type (str): MIME type of the attachment.
            size (int): Size in bytes (defaults to ``len(content)`` for raw bytes).
        """
        if isinstance(content, (bytes, bytearray)):
            size = len(content) if size is None else size
            content_bytes = base64.b64encode(bytes(content)).decode("ascii")
        else:
            content_bytes = content

        return_type = TaskFileAttachment(self.context, EntityPath(None, self.resource_path))
        return_type.set_property("name", name)
        return_type.set_property("contentBytes", content_bytes)
        if content_type is not None:
            return_type.set_property("contentType", content_type)
        if size is not None:
            return_type.set_property("size", size)

        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Tasks.ReadWrite"])
    def create_upload_session(
        self,
        name: str,
        size: int,
        content_type: Optional[str] = None,
    ) -> AttachmentSession:
        """Create an upload session for a file larger than 3 MB (up to 25 MB).

        Args:
            name (str): Display name of the attachment.
            size (int): Size in bytes of the file to upload.
            content_type (str): MIME type of the file.
        """
        attachment_info = AttachmentInfo(
            attachmentType=AttachmentType.file,
            contentType=content_type,
            name=name,
            size=size,
        )
        return_type = AttachmentSession(self.context)
        qry = ServiceOperationQuery(
            self, "createUploadSession", None, {"attachmentInfo": attachment_info}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
