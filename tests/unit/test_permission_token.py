"""A token answers a requirement where it can, and says so where it cannot.

The probe in :meth:`tests.capabilities.TenantState.of` reads the client's own token before it
asks the tenant, because the token is what the wire will judge. That preference is only safe if
the token is refused exactly where it is silent: another API's audience, the other flow, or no
readable token at all - each of those must fall back to the grants rather than answer "not
granted".

Measured against a real tenant, this is the difference between a suite that skips 25 of its 355
requirements for a reason that does not exist (a Graph grant read cannot see `Mail.Send`, which
Exchange grants) and one that skips none of them.
"""

from __future__ import annotations

import base64
import json
from typing import Any
from unittest import TestCase

from office365.directory.permissions.guard import _cached_delegated_permissions
from office365.permissions import Requirement, ResourceName, TokenClaims
from office365.permissions.token import _AUDIENCES
from tests.capabilities import TenantState

CLIENT_ID = "11111111-1111-1111-1111-111111111111"

GRAPH_AUDIENCE = "https://graph.microsoft.com"
SHAREPOINT_AUDIENCE = "00000003-0000-0ff1-ce00-000000000000"


def _jwt(**claims: Any) -> str:
    """An unsigned JWT with ``claims`` as its payload - the part a reader reads."""

    def _encode(payload: dict[str, Any]) -> str:
        return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    return f"{_encode({'alg': 'RS256', 'typ': 'JWT'})}.{_encode(claims)}.signature"


def test_a_users_token_states_its_scopes_and_no_roles() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, scp="Mail.Read Mail.Send"))

    assert claims is not None
    assert claims.audience == GRAPH_AUDIENCE
    assert claims.delegated == frozenset({"Mail.Read", "Mail.Send"})
    assert claims.application is None  # the claim is absent: this is not an app-only token


def test_an_app_only_token_states_its_roles_and_no_scopes() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, roles=["Mail.Read", "Sites.ReadWrite.All"]))

    assert claims is not None
    assert claims.application == frozenset({"Mail.Read", "Sites.ReadWrite.All"})
    assert claims.delegated is None


def test_a_token_proves_a_requirement_for_its_own_audience() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, roles=["Mail.Send"]))

    assert claims is not None
    assert claims.proves(Requirement(application=("Mail.Send",))) == frozenset({"Mail.Send"})


def test_a_token_cannot_speak_for_another_api() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, roles=["Mail.Send"]))

    assert claims is not None
    # the same name is a different grant on SharePoint, and this token was not issued for it
    assert claims.proves(Requirement(application=("Mail.Send",), resource=ResourceName.SharePoint)) is None


def test_a_token_cannot_speak_for_the_other_flow() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, scp="Mail.Read"))

    assert claims is not None
    assert claims.proves(Requirement(application=("Mail.Send",))) is None


def test_a_sharepoint_token_proves_its_own_audience() -> None:
    claims = TokenClaims.parse(_jwt(aud=f"{SHAREPOINT_AUDIENCE}@12345678-1234-1234-1234-123456789012", roles=[]))

    assert claims is not None
    # a legacy ACS token appends the realm to the app id; the API is still SharePoint
    assert claims.proves(Requirement(application=("Sites.FullControl.All",), resource=ResourceName.SharePoint)) == (
        frozenset()
    )


def test_an_api_with_no_known_audience_is_never_proved() -> None:
    claims = TokenClaims.parse(_jwt(aud=GRAPH_AUDIENCE, roles=["Mail.Send"]))

    assert claims is not None
    assert "Dynamics CRM" not in _AUDIENCES
    assert claims.proves(Requirement(application=("Mail.Send",), resource=ResourceName.Dynamics)) is None


def test_an_opaque_token_proves_nothing() -> None:
    assert TokenClaims.parse("eyJhbGciOiJSUzI1NiJ9") is None  # one part: not a JWT
    assert TokenClaims.parse("not.a.jwt") is None  # the payload is not JSON
    assert TokenClaims.parse("") is None
    assert TokenClaims.parse(None) is None


def test_a_payload_that_is_not_an_object_proves_nothing() -> None:
    payload = base64.urlsafe_b64encode(b"[1, 2]").decode().rstrip("=")

    assert TokenClaims.parse(f"header.{payload}.signature") is None


class _Context:
    """The request context a client holds its token in - the only public way to reach it."""

    def __init__(self, access_token: str | None) -> None:
        self.access_token = access_token


class _Request:
    def __init__(self, access_token: str | None) -> None:
        self.authentication_context = _Context(access_token)


class _Granted:
    """A resource's service principal, recording that it was asked."""

    def __init__(self, delegated: list[str]) -> None:
        self.delegated = delegated

    def get_delegated_permissions(self, client_id: str) -> Any:
        result = type("Result", (), {})()
        result.value = list(self.delegated)
        result.execute_query = lambda: result
        return result


class _Principals:
    def __init__(self, delegated: list[str]) -> None:
        self.granted = _Granted(delegated)
        self.asked: list[str] = []

    def find_by_name(self, name: Any, *, required: bool = False) -> _Granted:
        self.asked.append(str(name))
        return self.granted


class _Client:
    """A client holding ``token`` whose tenant grants are ``delegated`` on every resource."""

    def __init__(self, token: str | None, delegated: list[str]) -> None:
        self.token = token
        self.service_principals = _Principals(delegated)

    def pending_request(self) -> _Request:
        return _Request(self.token)


class TestWhatTheProbeAsks(TestCase):
    """The probe reads the token first, and only falls back where the token is silent."""

    def tearDown(self) -> None:
        for cached in (_cached_delegated_permissions,):
            cached.cache_clear()

    def test_a_token_answers_without_asking_the_tenant(self):
        client = _Client(_jwt(aud=GRAPH_AUDIENCE, scp="Mail.Send"), delegated=["Mail.Read"])

        state = TenantState.of(client, CLIENT_ID, Requirement(delegated=("Mail.Send",)))

        self.assertEqual(state.delegated, frozenset({"Mail.Send"}))
        self.assertEqual(client.service_principals.asked, [])

    def test_a_token_for_another_api_sends_the_probe_to_the_tenant(self):
        client = _Client(_jwt(aud=GRAPH_AUDIENCE, scp="Mail.Send"), delegated=["AllSites.FullControl"])

        state = TenantState.of(
            client, CLIENT_ID, Requirement(delegated=("AllSites.FullControl",), resource=ResourceName.SharePoint)
        )

        self.assertEqual(state.delegated, frozenset({"AllSites.FullControl"}))
        self.assertEqual(client.service_principals.asked, [ResourceName.SharePoint.value])

    def test_an_opaque_token_sends_the_probe_to_the_tenant(self):
        client = _Client("an-opaque-token", delegated=["Mail.Read"])

        state = TenantState.of(client, CLIENT_ID, Requirement(delegated=("Mail.Read",)))

        self.assertEqual(state.delegated, frozenset({"Mail.Read"}))
        self.assertEqual(client.service_principals.asked, [ResourceName.Graph.value])

    def test_a_client_that_cannot_hold_a_token_asks_the_tenant(self):
        client = type("Client", (), {"service_principals": _Principals(["Mail.Read"])})()

        state = TenantState.of(client, CLIENT_ID, Requirement(delegated=("Mail.Read",)))

        self.assertEqual(state.delegated, frozenset({"Mail.Read"}))

    def test_a_token_that_names_none_of_the_scopes_is_an_answer_not_a_silence(self):
        """The token carries ``scp`` and it does not include the scope: that is a real "no".

        Falling back here would hide a genuine shortfall behind the tenant's grants - the token
        is the identity that will send the request.
        """
        client = _Client(_jwt(aud=GRAPH_AUDIENCE, scp="Mail.Read"), delegated=["Mail.Send"])

        state = TenantState.of(client, CLIENT_ID, Requirement(delegated=("Mail.Send",)))

        self.assertFalse(Requirement(delegated=("Mail.Send",)).satisfied_by(state))
        self.assertEqual(client.service_principals.asked, [])
