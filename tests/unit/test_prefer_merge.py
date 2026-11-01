"""``Prefer`` is one header, so layering a preference must merge rather than replace.

A request carries a single comma-separated ``Prefer`` value. Two callers that each
``set`` it would silently drop the first, which is why :func:`add_prefer` appends
instead — and why a preference the caller attached by hand survives the one a
query capability requires.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.http.prefer import (
    BYPASS_SHARED_LOCK,
    RESPOND_ASYNC,
    RETURN_REPRESENTATION,
    TRY_FILTER_LAST_MODIFIED_DATE_TIME,
    add_prefer,
    prefer_create_if_missing,
    prefer_return_representation,
)
from office365.runtime.http.request_options import RequestOptions
from tests._scripted_transport import RecordingTransport


def _request(prefer: str | None = None) -> RequestOptions:
    request = RequestOptions("https://graph.microsoft.com/v1.0/me")
    if prefer is not None:
        request.set_header("Prefer", prefer)
    return request


def test_two_preferences_are_comma_joined_in_order():
    request = _request()
    prefer_create_if_missing(request)
    prefer_return_representation(request)

    assert request.headers["Prefer"] == f"create-if-missing, {RETURN_REPRESENTATION}"


def test_a_value_already_present_is_not_duplicated():
    request = _request(f"{BYPASS_SHARED_LOCK}, {RESPOND_ASYNC}")
    add_prefer(request, RESPOND_ASYNC, RETURN_REPRESENTATION)

    assert request.headers["Prefer"] == f"{BYPASS_SHARED_LOCK}, {RESPOND_ASYNC}, {RETURN_REPRESENTATION}"


def test_nothing_is_attached_when_no_value_is_given():
    request = _request()
    add_prefer(request, "")

    assert "Prefer" not in request.headers


def test_a_caller_preference_survives_the_one_the_query_requires():
    """The collection layers its capability's preference on top of the caller's."""
    transport = RecordingTransport([{"value": []}])
    client = GraphClient()
    request = client.pending_request()
    request.beforeExecute.clear()
    request.transport = transport
    request.before_execute(lambda options: options.set_header("Prefer", RESPOND_ASYNC))

    client.me.drive.root.children.filter("lastModifiedDateTime gt 2020-01-01T00:00:00Z").get().execute_query()

    values = [value.strip() for value in transport.requests[-1].headers["Prefer"].split(",")]
    assert values == [RESPOND_ASYNC, TRY_FILTER_LAST_MODIFIED_DATE_TIME]
