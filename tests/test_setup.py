"""Offline pins for the choices `tests.setup` makes before it touches the network.

The wizard is the one program that writes `.env`, and every branch in it used to be
reachable only by answering a prompt, so none of it was tested. `-y` turns every
prompt into its default, which keeps this a pure decision test: no client, no
terminal, no `.env` on disk.
"""

from __future__ import annotations

import unittest
from argparse import ArgumentParser, Namespace
from typing import cast
from unittest import mock

from office365.graph_client import GraphClient

from tests import preflight, setup
from tests._scripted_transport import RecordingTransport
from tests.capabilities import Requirement, TenantState
from tests.settings import Settings, settings


def _resolve(argv: list[str], existing: dict[str, str] | None = None) -> setup._Options:
    """Parse `argv` as a non-interactive run and resolve the wizard's options."""
    parser = setup._build_parser()
    args = parser.parse_args([*argv, "-y"])
    return setup._resolve_options(args, parser, existing or {})


def _client(*payloads) -> tuple[GraphClient, RecordingTransport]:
    """A Graph client whose every call answers the next scripted payload."""
    transport = RecordingTransport(list(payloads))
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


class TestResolveOptions(unittest.TestCase):
    def test_a_non_interactive_run_takes_its_defaults_from_the_environment(self) -> None:
        opts = _resolve(["--tenant", "contoso.onmicrosoft.com", "--client-id", "app-id"])
        self.assertEqual(opts.tenant, "contoso.onmicrosoft.com")
        self.assertEqual(opts.client_id, "app-id")
        self.assertEqual(opts.sites_scope, "all")
        self.assertEqual(opts.site_urls, [])
        self.assertFalse(opts.extras)
        self.assertFalse(opts.want_secret)
        self.assertEqual(opts.app_name, setup.DEFAULT_APP_NAME)
        self.assertEqual(opts.username, settings.username)
        self.assertEqual(opts.password, settings.password)

    def test_a_site_url_implies_the_selected_scope(self) -> None:
        opts = _resolve(["--tenant", "t", "--client-id", "c", "--site", "https://a", "--site", "https://b"])
        self.assertEqual((opts.sites_scope, opts.site_urls), ("selected", ["https://a", "https://b"]))

    def test_an_explicit_empty_value_is_not_a_fallback(self) -> None:
        opts = _resolve(["--tenant", "t", "--client-id", "c", "--username", "bob", "--username-alt", ""])
        self.assertEqual(opts.username, "bob")
        self.assertEqual(opts.username_alt, "")
        self.assertTrue(opts.extras, "asking for a value, even empty, is asking for the optional block")

    def test_no_secret_wins_over_with_secret(self) -> None:
        opts = _resolve(["--tenant", "t", "--client-id", "c", "--with-secret", "--no-secret"])
        self.assertFalse(opts.want_secret)

    def test_rotating_a_secret_is_asking_for_a_secret(self) -> None:
        opts = _resolve(["--tenant", "t", "--client-id", "c", "--rotate-secret", "key-id"])
        self.assertTrue(opts.want_secret, "--rotate-secret deletes and creates, so it cannot be a no-op")
        self.assertEqual(opts.rotate_secret, "key-id")

    def test_an_application_secret_already_in_the_file_is_reused(self) -> None:
        opts = _resolve(["--tenant", "t", "--client-id", "c"], {"OFFICE365_CLIENT_SECRET": "kept"})
        self.assertFalse(opts.want_secret)

    def test_the_configured_tenant_is_the_default(self) -> None:
        configured = Settings(tenant="contoso.onmicrosoft.com", client_id="app-id", admin_username="admin@contoso.com")
        with mock.patch.object(setup, "settings", configured):
            opts = _resolve([])
        self.assertEqual(
            (opts.tenant, opts.client_id, opts.admin), ("contoso.onmicrosoft.com", "app-id", "admin@contoso.com")
        )

    def test_a_missing_tenant_fails_instead_of_prompting_when_non_interactive(self) -> None:
        parser = setup._build_parser()
        args: Namespace = parser.parse_args(["--client-id", "c", "-y"])
        with mock.patch.object(setup, "settings", Settings()), self.assertRaises(SystemExit) as raised:
            setup._resolve_options(args, parser, {})
        self.assertEqual(raised.exception.code, 2)

    def test_an_unparseable_option_is_rejected_by_the_parser(self) -> None:
        with self.assertRaises(SystemExit):
            _resolve(["--tenant", "t", "--client-id", "c", "--sites", "some"])
        self.assertIsInstance(setup._build_parser(), ArgumentParser)


class _StubQuery:
    def execute_query(self) -> None:
        return None


class _GrantClient:
    """The four calls `--grant` makes, scripted: nothing is sent, the decisions are pinned."""

    def __init__(self, granted: tuple[str, ...] = (), refuse: tuple[str, ...] = ()) -> None:
        self.granted = set(granted)
        self.refuse = set(refuse)
        self.calls: list[str] = []

    def has_delegated_permission(self, scope: str, app_id: str) -> bool:
        return scope in self.granted

    def has_application_permissions(self, name: str, app_id: str) -> bool:
        return name in self.granted

    def grant_delegated_permissions(self, app_id: str, scope: str) -> _StubQuery:
        return self._grant(f"delegated {scope}", scope)

    def grant_application_permissions(self, app_id: str, name: str) -> _StubQuery:
        return self._grant(f"application {name}", name)

    def _grant(self, entry: str, name: str) -> _StubQuery:
        self.calls.append(entry)
        if name in self.refuse:
            raise setup.ClientRequestException("Forbidden")
        return _StubQuery()


class TestGrant(unittest.TestCase):
    """Granting what the suites declare: only what is missing, and a refusal does not stop the rest."""

    def test_each_missing_permission_is_granted_once(self) -> None:
        client = _GrantClient()
        plan = {"delegated": ["Mail.Read"], "application": ["Domain.Read.All"]}
        done, failed = setup._apply_grants(cast(GraphClient, client), "app-id", plan)
        self.assertEqual(done, ["delegated Mail.Read", "application Domain.Read.All"])
        self.assertEqual(failed, [])
        self.assertEqual(client.calls, ["delegated Mail.Read", "application Domain.Read.All"])

    def test_a_permission_that_is_already_granted_is_not_granted_again(self) -> None:
        client = _GrantClient(granted=("Mail.Read",))
        done, _ = setup._apply_grants(cast(GraphClient, client), "app-id", {"delegated": ["Mail.Read"]})
        self.assertEqual(done, ["delegated Mail.Read (already granted)"])
        self.assertEqual(client.calls, [])

    def test_a_refused_grant_is_reported_and_the_next_one_is_still_attempted(self) -> None:
        client = _GrantClient(refuse=("Mail.Read",))
        plan = {"delegated": ["Mail.Read", "Files.Read"]}
        done, failed = setup._apply_grants(cast(GraphClient, client), "app-id", plan)
        self.assertEqual(done, ["delegated Files.Read"])
        self.assertEqual(len(failed), 1)
        self.assertTrue(failed[0].startswith("delegated Mail.Read: Forbidden"))

    def test_a_dry_run_prints_the_plan_and_grants_nothing(self) -> None:
        requirement = Requirement(delegated=("Mail.Read",))
        found = [preflight.Needs(suite="tests/x/test_y.py", flow="delegated-ropc", tests=1)]
        found[0].add(requirement, "Suite.test_scoped")
        with mock.patch.object(setup.preflight, "suites", return_value=found):
            with mock.patch.object(setup.preflight, "verify", return_value={requirement: TenantState()}):
                with mock.patch.object(setup, "_sign_in") as sign_in:
                    self.assertEqual(setup.main(["--grant", "--dry-run", "-y"]), 0)
        sign_in.assert_not_called()


class TestDiscovery(unittest.TestCase):
    """The two best-effort lookups: they ask for the column they read, and a refusal is empty."""

    def test_the_user_list_asks_for_the_upn_it_reads_and_skips_the_rest(self) -> None:
        client, transport = _client(
            {"value": [{"userPrincipalName": "a@contoso.com"}, {"id": "no-upn"}, {"userPrincipalName": "b@contoso.com"}]}
        )
        self.assertEqual(setup._list_users(client), ["a@contoso.com", "b@contoso.com"])
        self.assertEqual(transport.urls, ["https://graph.microsoft.com/v1.0/users?$select=userPrincipalName&$top=25"])

    def test_a_refused_lookup_answers_empty_instead_of_failing(self) -> None:
        signed_in = setup._signed_in_upn(_client(("deny",))[0])
        users = setup._list_users(_client(("deny",))[0])
        self.assertEqual((signed_in, users), ("", []))


if __name__ == "__main__":
    unittest.main()
