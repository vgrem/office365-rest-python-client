import os
from functools import partial
from typing import IO, AnyStr, Callable, Dict, Optional, Union

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.attachments.creation_information import (
    AttachmentCreationInformation,
)
from office365.sharepoint.entity_collection import EntityCollection


class AttachmentCollection(EntityCollection[Attachment]):
    """Represents a collection of Attachment resources for a SharePoint list item."""

    def __init__(self, context, resource_path=None, parent=None):
        """
        Initialize an attachment collection

        Args:
            context: Client context
            resource_path: Resource path for attachments
            parent: Parent list item
        """
        super().__init__(context, Attachment, resource_path, parent)

    def add(
        self, attachment_file_information: Union[AttachmentCreationInformation, Dict]
    ) -> Attachment:
        """
        Adds the attachment represented by the file name and stream in the specified parameter to the list item.

        :param AttachmentCreationInformation attachment_file_information: The creation information which contains file
            name and content stream.
        """
        if isinstance(attachment_file_information, dict):
            attachment_file_information = AttachmentCreationInformation(
                attachment_file_information.get("filename"),
                attachment_file_information.get("content"),
            )

        return_type = Attachment(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(
            self,
            "add",
            {
                "filename": attachment_file_information.filename,
            },
            attachment_file_information.content,
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def add_using_path(self, decoded_url: str, content_stream: bytes) -> Attachment:
        """
        Adds an attachment using a decoded URL path.

        Args:
            decoded_url: Path for the attachment file
            content_stream: Attachment content as bytes

        Returns:
            The created Attachment object
        """
        return_type = Attachment(self.context)
        params = {"DecodedUrl": decoded_url}
        qry = ServiceOperationQuery(
            self, "AddUsingPath", params, content_stream, None, return_type
        )
        self.context.add_query(qry)
        self.add_child(return_type)
        return return_type

    def delete_all(self):
        """Deletes all attachments"""

        def _delete_all(return_type: "AttachmentCollection") -> None:
            [a.delete_object() for a in return_type]

        self.get().after_execute(_delete_all)
        return self

    def download(
        self,
        output_file: IO[bytes],
        file_downloaded: Optional[Callable[[Attachment], None]] = None,
    ) -> Self:
        """
        Downloads all attachments as a ZIP file.

        Args:
            output_file: File-like object to write ZIP content to
            file_downloaded: Optional callback after each file download
        """
        import zipfile

        def _file_downloaded(
            attachment_file: Attachment, result: ClientResult[AnyStr]
        ) -> None:
            with zipfile.ZipFile(output_file.name, "a", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(attachment_file.file_name, result.value)
                if callable(file_downloaded):
                    file_downloaded(attachment_file)

        def _download(return_type):
            for attachment_file in return_type:
                attachment_file.get_content().after_execute(
                    partial(_file_downloaded, attachment_file)
                )

        self.get().after_execute(_download)
        return self

    def upload(self, file: IO[bytes], use_path: bool = True) -> Attachment:
        """
        Uploads a file as an attachment.

        Args:
            file: File-like object to upload
            use_path: Whether to use path-based upload

        Returns:
            The created Attachment object
        """
        filename = os.path.basename(file.name)
        content = file.read()
        if use_path:
            return self.add_using_path(filename, content)
        else:
            return self.add(AttachmentCreationInformation(filename, content))

    def get_by_filename(self, filename: str) -> Attachment:
        """
        Gets an attachment by filename.

        Args:
            filename: Name of the attachment file

        Returns:
            Attachment object
        """
        return Attachment(
            self.context,
            ServiceOperationPath("GetByFileName", [filename], self.resource_path),
        )

    def get_by_filename_as_path(self, decoded_url: str) -> Attachment:
        """
        Gets an attachment by decoded URL path.

        Args:
            decoded_url: Decoded URL path to the file

        Returns:
            Attachment object
        """
        return Attachment(
            self.context,
            ServiceOperationPath(
                "GetByFileNameAsPath", [decoded_url], self.resource_path
            ),
        )
