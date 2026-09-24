"""Tests for SharePoint client-context authentication wiring (offline)."""

from __future__ import annotations

import pytest
from office365.sharepoint.client_context import ClientContext


def test_with_user_credentials_raises_for_sharepoint_online():
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    with pytest.raises(RuntimeError, match="legacy SAML/ACS"):
        ctx.with_user_credentials("user@contoso.com", "pwd")


def test_with_user_credentials_uses_ntlm_when_allowed(monkeypatch):
    monkeypatch.setattr(
        "office365.runtime.auth.providers.ntlm_provider.NtlmProvider.__init__",
        lambda self, credentials, *args, **kwargs: None,
    )
    ctx = ClientContext("https://sp2019.contoso.local", allow_ntlm=True)

    ctx.with_user_credentials("DOMAIN\\user", "pwd")  # must not raise

    assert callable(ctx.authentication_context._authenticate)
