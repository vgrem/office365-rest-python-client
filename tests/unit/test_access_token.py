"""The token a context holds, read for what it proves rather than to make a request.

A live test that wants to know whether the wire will accept its call needs the token that will
be sent, and it usually wants that answer *before* sending anything. So reading the property
acquires the token once - cached, exactly as a request would leave it - which also means the
answer cannot depend on whether a request happened to run first.

The alternative, acquiring only on the first request, made the same test skip or run depending on
its position in the suite, which is not a property a skip decision may have.
"""

from __future__ import annotations

from typing import Any

from office365.runtime.auth.authentication_context import AuthenticationContext as RequestContext
from office365.runtime.auth.entra.authentication_context import AuthenticationContext as EntraContext

TOKEN = "header.payload.signature"
URL = "https://contoso.sharepoint.com"


class _Counter:
    """A token callback that counts how often it was asked."""

    def __init__(self, token: Any = TOKEN) -> None:
        self.calls = 0
        self.token = token

    def __call__(self) -> Any:
        self.calls += 1
        return {"access_token": self.token, "expires_in": 3600}


def test_reading_the_token_of_a_request_context_acquires_it_once():
    callback = _Counter()
    context = RequestContext(URL).with_access_token(callback)

    assert context.access_token == TOKEN
    assert context.access_token == TOKEN
    assert callback.calls == 1


def test_reading_the_token_of_an_entra_context_acquires_it_once():
    callback = _Counter()
    context = EntraContext(tenant="contoso.onmicrosoft.com").with_access_token(callback)

    assert context.access_token == TOKEN
    assert context.access_token == TOKEN
    assert callback.calls == 1


def test_a_context_with_no_token_callback_answers_none():
    """A cookie-authenticated context has no bearer token; that is not an error."""
    assert RequestContext(URL).access_token is None
    assert EntraContext(tenant="contoso.onmicrosoft.com").access_token is None


def test_an_async_callback_is_not_awaited_from_a_synchronous_read():
    async def callback() -> dict[str, Any]:
        return {"access_token": TOKEN, "expires_in": 3600}

    assert EntraContext(tenant="contoso.onmicrosoft.com").with_access_token(callback).access_token is None
    assert RequestContext(URL).with_access_token(callback).access_token is None
