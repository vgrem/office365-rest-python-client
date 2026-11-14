"""Pure regressions behind fixed issues - each one a function, not a request.

- #884/#978: a quote inside an OData literal is doubled, while slashes and spaces in a
  server-relative path stay literal instead of being %-encoded into the call syntax.
- #793: the upload length of a stream comes from its size, and seeking it back is optional.
- #875: a sharing token is base64url with every ``=`` stripped, not just one or two.
"""

from __future__ import annotations

import base64
import io
import os
import tempfile

import pytest
from office365.onedrive.internal.paths.shared import _url_to_shared_token
from office365.runtime.paths.builder import ODataPathBuilder
from office365.sharepoint.files.collection import _stream_size


def test_an_odata_string_literal_doubles_a_quote_and_keeps_a_path_readable():
    """A quote is escaped by doubling; slashes and spaces stay literal rather than %-encoded."""
    assert ODataPathBuilder._encode_odata_value("macdonald's file.txt") == "'macdonald''s file.txt'"
    assert ODataPathBuilder._encode_odata_value("/sites/x/a b/c.txt") == "'/sites/x/a b/c.txt'"


class _Unseekable(io.BytesIO):
    def seek(self, *args, **kwargs):
        raise io.UnsupportedOperation("seek")


def test_the_upload_length_of_a_stream_is_its_size_and_the_position_survives():
    stream = io.BytesIO(b"x" * 12345)
    stream.seek(2)

    assert _stream_size(stream) == 12345  # noqa: PLR2004
    assert stream.tell() == 2  # noqa: PLR2004 - the caller keeps reading where it was


def test_a_real_file_reports_its_size():
    with tempfile.NamedTemporaryFile(delete=False) as handle:
        handle.write(b"y" * 777)
        path = handle.name
    try:
        with open(path, "rb") as stream:
            assert _stream_size(stream) == 777  # noqa: PLR2004
    finally:
        os.unlink(path)


def test_a_stream_that_cannot_seek_is_refused_rather_than_guessed():
    with pytest.raises(ValueError, match="seekable"):
        _stream_size(_Unseekable(b"data"))


def test_every_base64_pad_is_stripped_from_a_sharing_token():
    url = "https://a"
    encoded = base64.b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    expected = "u!" + encoded.replace("/", "_").replace("+", "-")

    token = _url_to_shared_token(url)

    assert token == expected
    assert "=" not in token
