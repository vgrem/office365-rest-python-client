"""Offline tests for upload-stream size handling (refs issue #793)."""

from __future__ import annotations

import io
import os
import tempfile

import pytest
from office365.sharepoint.files.collection import _stream_size


class _Unseekable(io.BytesIO):
    def seek(self, *args, **kwargs):
        raise io.UnsupportedOperation("seek")


def test_stream_size_from_bytesio():
    data = b"x" * 12345
    stream = io.BytesIO(data)
    assert _stream_size(stream) == len(data)
    assert stream.tell() == 0  # position preserved


def test_stream_size_from_bytesio_mid_stream():
    stream = io.BytesIO(b"abcdef")
    offset = 2
    stream.seek(offset)
    assert _stream_size(stream) == 6  # noqa: PLR2004
    assert stream.tell() == offset  # position preserved


def test_stream_size_from_real_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"y" * 777)
        path = f.name
    try:
        with open(path, "rb") as f:
            assert _stream_size(f) == 777  # noqa: PLR2004
    finally:
        os.unlink(path)


def test_stream_size_rejects_unseekable_source():
    with pytest.raises(ValueError, match="seekable"):
        _stream_size(_Unseekable(b"data"))
