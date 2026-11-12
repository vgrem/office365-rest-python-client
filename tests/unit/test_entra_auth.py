"""Tests for the Entra (Graph) authentication context device flow (offline)."""

from __future__ import annotations

import json
import sys
import types

import pytest
from office365.cli import main
from office365.graph_client import GraphClient
from office365.runtime.auth.entra.authentication_context import AuthenticationContext

#: What argparse exits with when it cannot build a command at all.
USAGE_ERROR = 2


class _FakePublicClientApplication:
    """Minimal MSAL stand-in that records device-flow / silent acquisition calls."""

    def __init__(self, client_id, authority=None, **kwargs):
        self.accounts: list[dict] = []
        self.silent_result: dict | None = {"access_token": "cached"}
        self.initiated = 0
        self.silent_calls = 0
        self.kwargs = kwargs

    def get_accounts(self, username=None):
        return list(self.accounts)

    def acquire_token_silent(self, scopes, account=None, **kwargs):
        self.silent_calls += 1
        return self.silent_result

    def initiate_device_flow(self, scopes=None, **kwargs):
        self.initiated += 1
        return {"user_code": "ABCD", "message": "visit https://microsoft.com/devicelogin and enter ABCD"}

    def acquire_token_by_device_flow(self, flow):
        self.accounts.append({"home_account_id": "account-1"})
        return {"access_token": "device", "expires_in": 3600}


class _FakeTokenCache:
    """The one thing a session store needs from MSAL's cache: it serializes."""

    def serialize(self):
        return '{"AccessToken": {}}'


def _install_fake_msal(monkeypatch) -> list[_FakePublicClientApplication]:
    created: list[_FakePublicClientApplication] = []

    def _factory(*args, **kwargs):
        app = _FakePublicClientApplication(*args, **kwargs)
        created.append(app)
        return app

    fake = types.ModuleType("msal")
    fake.PublicClientApplication = _factory  # type: ignore[attr-defined]
    fake.SerializableTokenCache = _FakeTokenCache  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "msal", fake)
    return created


def test_device_flow_prompts_once_then_reuses_cached_token(monkeypatch):
    created = _install_fake_msal(monkeypatch)
    ctx = AuthenticationContext(tenant="contoso.onmicrosoft.com")
    ctx.with_device_flow("client-id")
    acquire = ctx._token_callback
    assert acquire is not None

    assert acquire()["access_token"] == "device"
    assert acquire()["access_token"] == "cached"

    app = created[0]
    assert app.initiated == 1
    assert app.silent_calls == 1


def test_a_public_client_flow_hands_the_cache_to_msal(monkeypatch):
    created = _install_fake_msal(monkeypatch)
    cache = object()
    ctx = AuthenticationContext(tenant="contoso.onmicrosoft.com", token_cache=cache)

    ctx.with_device_flow("client-id")
    ctx.with_token_interactive("client-id")
    ctx.with_username_and_password("client-id", "ann@contoso.com", "secret")

    # Without this the login dies with the process: only the confidential flows
    # used to receive it, and a command line can use neither of them.
    assert [app.kwargs.get("token_cache") for app in created] == [cache, cache, cache]


def test_the_client_hands_its_cache_and_scopes_to_the_context():
    cache = object()
    client = GraphClient(tenant="contoso.onmicrosoft.com", scopes=["User.Read"], token_cache=cache)

    # Both used to stop at the client: the request carried neither, so the cache was
    # unread and the scopes silently became the *.default one.
    context = client.pending_request().authentication_context
    assert context._token_cache is cache
    assert context._scopes == ["User.Read"]
    assert GraphClient().pending_request().authentication_context._scopes == ["https://graph.microsoft.com/.default"]


def test_a_login_is_kept_and_answers_whoami(monkeypatch, tmp_path):
    _install_fake_msal(monkeypatch)
    monkeypatch.setenv("O365_HOME", str(tmp_path))

    assert main(["login", "--tenant", "contoso.onmicrosoft.com", "--client-id", "cli-client"]) == 0
    kept = json.loads((tmp_path / "sessions.json").read_text("utf-8"))["graph"]
    assert kept["method"] == "with_device_flow"
    assert kept["client_id"] == "cli-client"
    assert kept["constructor"] == {"tenant": "contoso.onmicrosoft.com"}
    assert kept["cache"] == '{"AccessToken": {}}'
    assert not (tmp_path / "sessions.json").stat().st_mode & 0o077

    # A second command reads what the first wrote, without logging in again.
    assert main(["whoami"]) == 0
    assert main(["logout"]) == 0
    assert main(["whoami"]) == 1

    # The library ships no app registration of its own, so this cannot be filled in.
    with pytest.raises(SystemExit) as refused:
        main(["login", "--tenant", "contoso.onmicrosoft.com"])
    assert refused.value.code == USAGE_ERROR
