"""An in-memory upload over the chunk size is read from memory, not staged to disk.

The simple path takes the bytes directly; a resumable session needs a stream, and the
stream a caller's ``bytes`` becomes is the caller's own content — nothing is written to a
temporary file on the way (upstream #1077).
"""

from __future__ import annotations

import io
from unittest import mock

from office365.migration.offline import offline_sharepoint_context
from office365.sharepoint.files.collection import FileCollection

#: Larger than the chunk size below, so the session path is taken.
CONTENT = b"0123456789abcdefghijKLMNO"


def _folder():
    return offline_sharepoint_context().web.get_folder_by_server_relative_path("/sites/x/Shared Documents")


def test_content_over_the_chunk_size_is_handed_over_as_a_readable_stream():
    with mock.patch.object(FileCollection, "create_upload_session", autospec=True) as session:
        _folder().files.upload_content(CONTENT, "big.bin", chunk_size=10)

    _, stream = session.call_args.args
    assert isinstance(stream, io.IOBase)
    assert stream.read() == CONTENT
    assert session.call_args.kwargs["file_name"] == "big.bin"


def test_content_within_the_chunk_size_never_opens_a_session():
    with (
        mock.patch.object(FileCollection, "create_upload_session") as session,
        mock.patch.object(FileCollection, "_simple_upload") as simple,
    ):
        _folder().files.upload_content(CONTENT, "small.bin", chunk_size=len(CONTENT))

    session.assert_not_called()
    assert simple.call_args.args[1] == CONTENT
