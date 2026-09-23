"""Tests for the SharePoint Site migration helpers (offline)."""

from __future__ import annotations

import base64

from office365.sharepoint.sites.site import _aes_key_base64


def test_aes_key_base64_passes_strings_through():
    key = base64.b64encode(bytes(range(32))).decode("ascii")
    assert _aes_key_base64(key) == key


def test_aes_key_base64_encodes_raw_bytes():
    raw = bytes(range(32))
    assert _aes_key_base64(raw) == base64.b64encode(raw).decode("ascii")
