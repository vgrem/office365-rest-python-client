import os
from typing import BinaryIO, Callable, Optional

from requests import Response
from typing_extensions import Self

from office365.runtime.client_request import ClientRequest
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.upload_session import UploadSessionQuery


class UploadSessionRequest(ClientRequest):
    """Handles file uploads in chunks using upload sessions."""

    def __init__(
        self,
        file_object: BinaryIO,
        chunk_size: int,
        chunk_uploaded: Callable[[int], None] = None,
    ) -> None:
        """Initialize an upload session request.

        Args:
            file_object: The file-like object to upload
            chunk_size: Size of each upload chunk in bytes
            chunk_uploaded: Callback invoked after each chunk is uploaded
        """
        super().__init__()
        self._file_object = file_object
        self._chunk_size = chunk_size
        self._chunk_uploaded = chunk_uploaded
        self._range_data: Optional[bytes] = None

    def build_request(self, query: UploadSessionQuery) -> Self:
        """Build a request for uploading a single chunk."""
        request = RequestOptions(query.upload_session_url)
        request.method = HttpMethod.Put
        request.set_header("Content-Length", str(len(self._range_data)))
        request.set_header(
            "Content-Range",
            f"bytes {self.range_start}-{self.range_end - 1}/{self.file_size}",
        )
        request.set_header("Accept", "*/*")
        request.data = self._range_data
        return request

    def process_response(self, response: Response, query: UploadSessionQuery) -> None:
        """Handle the response after uploading a chunk."""
        response.raise_for_status()
        if callable(self._chunk_uploaded):
            self._chunk_uploaded(self.range_end)

    def execute_query(self, query: UploadSessionQuery) -> Self:
        """Execute the upload query for each chunk."""
        for self._range_data in self._read_next():
            super().execute_query(query)
        return self

    def _read_next(self):
        """Generate fixed-size chunks from the file object.

        Yields:
            bytes: Chunks of data with maximum size of self._chunk_size
        """
        while True:
            chunk = self._file_object.read(self._chunk_size)
            if not chunk:
                break
            yield chunk

    @property
    def file_size(self) -> int:
        """Get the total size of the file being uploaded."""
        return os.fstat(self._file_object.fileno()).st_size

    @property
    def range_start(self) -> int:
        """Get the starting byte position of the current chunk."""
        if self.range_end == 0:
            return 0
        return self.range_end - len(self._range_data)

    @property
    def range_end(self) -> int:
        """Get the ending byte position of the current chunk."""
        return self._file_object.tell()
