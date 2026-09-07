"""Regression: sharing-token encoding must use UTF-8 bytes and drop all padding."""

from __future__ import annotations

import base64

from office365.onedrive.internal.paths.shared import _url_to_shared_token


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
