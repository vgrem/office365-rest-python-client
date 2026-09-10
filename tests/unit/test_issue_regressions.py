"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import base64
import io
import os
import tempfile
import unittest
import uuid
from unittest import mock

import pytest
from office365.graph_client import GraphClient
from office365.onedrive.internal.paths.shared import _url_to_shared_token
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.collection import _stream_size
from office365.sharepoint.files.file import File
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from requests import Response
from tests import test_site_url


class _CaptureTransport(BaseTransport):
    def __init__(self):
        super().__init__()
        self.url = ""

    def execute(self, request):
        self.url = request.url
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp.headers["Content-Type"] = "application/octet-stream"
        resp._content = b"payload"
        return resp


class TestFilePathQuoting(unittest.TestCase):
    """Apostrophes in server-relative paths must be escaped in the DecodedUrl literal."""

    def _context(self) -> tuple[ClientContext, _CaptureTransport]:
        ctx = ClientContext(test_site_url)
        transport = _CaptureTransport()
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport
        return ctx, transport

    def test_read_escapes_apostrophe(self):
        ctx, transport = self._context()
        result = File.open_binary(ctx, "/sites/x/Shared Documents/macdonald's file.txt")

        self.assertEqual(result.content, b"payload")
        self.assertIn("getFileByServerRelativePath", transport.url)
        self.assertIn("macdonald%27%27s", transport.url)

    def test_read_with_plain_path_unchanged(self):
        ctx, transport = self._context()
        result = File.open_binary(ctx, "/sites/x/Shared Documents/report.pdf")

        self.assertEqual(result.content, b"payload")
        self.assertIn("report.pdf", transport.url)
        self.assertNotIn("%27%27", transport.url)

    def test_write_escapes_apostrophe(self):
        ctx, transport = self._context()
        result = File.save_binary(ctx, "/sites/x/macdonald's file.txt", b"content")

        self.assertEqual(result.status_code, 200)
        self.assertIn("macdonald%27%27s", transport.url)


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


def _reference(url: str) -> str:
    b64 = base64.b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    return "u!" + b64.replace("/", "_").replace("+", "-")


def test_ascii_url_token_unchanged():
    url = "https://contoso.sharepoint.com/sites/team/shared%20doc.xlsx"
    assert _url_to_shared_token(url) == _reference(url)
    assert not _url_to_shared_token(url).endswith("=")


def test_non_ascii_url_token_uses_utf8():
    url = "https://contoso.sharepoint.com/sites/プロジェクト/資料.docx"
    assert _url_to_shared_token(url) == _reference(url)
    assert not _url_to_shared_token(url).endswith("=")


def test_all_base64_padding_is_removed():
    # a url whose base64 ends with '==' must leave no '=' in the token
    url = "https://a"
    token = _url_to_shared_token(url)
    assert token.startswith("u!")
    assert "=" not in token
    assert token == _reference(url)


def test_site_design_metadata_parses_non_empty_site_script_ids():
    design = SiteDesignMetadata()
    design.set_property(
        "SiteScriptIds",
        ["07702c07-0485-426f-b710-4704241caad9", "6250ceba-8724-4fb4-8c52-5a89183b9587"],
    )

    assert isinstance(design.SiteScriptIds, ClientValueCollection)
    assert len(design.SiteScriptIds) == 2  # noqa: PLR2004
    assert all(isinstance(item, uuid.UUID) for item in design.SiteScriptIds)


def test_site_design_metadata_parses_empty_collection():
    design = SiteDesignMetadata()
    design.set_property("SiteScriptIds", [])
    assert isinstance(design.SiteScriptIds, ClientValueCollection)
    assert len(design.SiteScriptIds) == 0


class _Result:
    def __init__(self, value):
        self.value = value

    def execute_query(self):
        return self

    def __iter__(self):
        return iter(self.value)


def _make_sku(part_number):
    sku = mock.Mock()
    sku.sku_part_number = part_number
    return sku


class TestRequireLicense(unittest.TestCase):
    def _make_client(self) -> GraphClient:
        return GraphClient(tenant="contoso.onmicrosoft.com")

    def test_passes_when_sku_matches(self):
        client = self._make_client()
        collection = mock.Mock()
        collection.get.return_value = _Result([_make_sku("BACKUP_STORAGE_ADDON"), _make_sku("ENTERPRISEPACK")])
        with mock.patch.object(GraphClient, "subscribed_skus", new_callable=mock.PropertyMock, return_value=collection):
            self.assertIs(client.require_license("BACKUP"), client)

    def test_exits_when_no_sku_matches(self):
        client = self._make_client()
        collection = mock.Mock()
        collection.get.return_value = _Result([_make_sku("ENTERPRISEPACK")])
        with mock.patch.object(GraphClient, "subscribed_skus", new_callable=mock.PropertyMock, return_value=collection):
            with self.assertRaises(SystemExit):
                client.require_license("BACKUP")

    def test_noop_without_keywords(self):
        client = self._make_client()
        self.assertIs(client.require_license(), client)


class TestRequireDelegatedPermission(unittest.TestCase):
    def _make_client(self) -> GraphClient:
        ctx = GraphClient(tenant="contoso.onmicrosoft.com")
        ctx.pending_request().authentication_context._client_id = "app-id"
        return ctx

    def test_passes_when_scope_granted(self):
        client = self._make_client()
        client.get_delegated_permissions = mock.Mock(  # type: ignore[method-assign]
            return_value=_Result(["User.Read", "Mail.Read"])
        )
        self.assertIs(client.require_delegated_permission("User.Read"), client)

    def test_exits_when_scope_missing(self):
        client = self._make_client()
        client.get_delegated_permissions = mock.Mock(  # type: ignore[method-assign]
            return_value=_Result(["Mail.Read"])
        )
        with self.assertRaises(SystemExit):
            client.require_delegated_permission("User.Read")

    def test_noop_without_scopes(self):
        client = self._make_client()
        self.assertIs(client.require_delegated_permission(), client)
