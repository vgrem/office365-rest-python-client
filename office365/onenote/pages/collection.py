from email.message import Message
from typing import IO, BinaryIO, Dict

from office365.entity_collection import EntityCollection
from office365.onenote.pages.page import OnenotePage
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.batch import create_boundary
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.utilities import get_mime_type


def _message_to_payload(message: Message) -> bytes:
    lf = b"\n"
    crlf = b"\r\n"
    payload = message.as_bytes()
    lines = payload.split(lf)
    payload = bytes.join(crlf, lines[2:]) + crlf
    return payload


class OnenotePageCollection(EntityCollection[OnenotePage]):
    """A collection of pages in a OneNote notebook"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, OnenotePage, resource_path)

    def add(self, presentation_file: IO, attachment_files: Dict[str, BinaryIO] = None) -> OnenotePage:
        """
        Create a new OneNote page.
        """

        return_type = OnenotePage(self.context)
        self.add_child(return_type)
        qry = ClientQuery(self.context, binding_type=self, return_type=return_type)

        def _construct_multipart_request(request: RequestOptions) -> None:
            request.method = HttpMethod.Post
            boundary = create_boundary("PageBoundary", True)
            request.set_header("Content-Type", f"multipart/form-data; boundary={boundary}")

            main_message = Message()
            main_message.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
            main_message.set_boundary(boundary)

            c_type, _enc = get_mime_type(presentation_file.name)
            presentation_message = Message()
            presentation_message.add_header("Content-Type", c_type)
            presentation_message.add_header("Content-Disposition", 'form-data; name="Presentation"')
            presentation_message.set_payload(presentation_file.read())
            main_message.attach(presentation_message)

            for name, file in attachment_files.items():
                file_message = Message()
                c_type, _enc = get_mime_type(file.name)
                file_message.add_header("Content-Type", c_type)
                file_message.add_header("Content-Disposition", f'form-data; name="{name}"')
                file_content = file.read()
                file_message.set_payload(file_content)
                main_message.attach(file_message)

            request.data = _message_to_payload(main_message)

        self.context.add_query(qry).before_query_execute(_construct_multipart_request)
        return return_type
