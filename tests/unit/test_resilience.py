"""What the runtime does when the service pushes back: retry, wait, throttle, refuse, and say why.

One file because the answer is one loop -- a 429 asks to come back, the limiter decides when,
the ceiling decides whether the call was even allowed, and the failure that survives carries
the text a caller reads. A limit and a retry are the same question asked at two timescales.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import warnings
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest import mock

import pytest
import requests
from office365.directory.invitations.invitation import Invitation
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.migration.offline import offline_sharepoint_context
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.permissions.permission import Permission
from office365.onenote.pages.page import OnenotePage
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.mail.folders.folder import MailFolder
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_request_exception import (
    ClientRequestException,
    ErrorPayload,
    _clean_message,
)
from office365.runtime.client_result import ClientResult
from office365.runtime.exceptions import FileLockedException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.http.throttling import (
    PaceState,
    RateLimiter,
    ThrottleLimits,
    pace,
    parse_throttling,
    throttle_guard,
)
from office365.runtime.limits import (
    Limit,
    LimitExceededError,
    LimitKind,
    bounded,
    catalog,
    catalog_products,
    ensure_within,
    limit,
    limits_of,
    verify_limits,
    warn_if_exceeds,
)
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.operations import ProgressTracker
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.retry import (
    backoff_delay,
    is_transient_error,
    response_retry_after,
    retry,
    should_reset_connections,
)
from office365.runtime.types.odata_property import odata
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.exceptions import SPQueryThrottledException
from office365.sharepoint.fields.field import Field
from office365.sharepoint.limits import LIST_VIEW_THRESHOLD, Limits
from office365.sharepoint.listitems.caml import Caml, CamlQuery
from office365.sharepoint.listitems.caml.guard import threshold_warnings, warn_if_unpaged
from office365.subscriptions.collection import SubscriptionCollection
from office365.subscriptions.subscription import Subscription
from office365.teams.chats.messages.message import ChatMessage
from requests import Response
from tests import test_site_url

LIST_VIEW = Limits.LIST_VIEW

#: What a row may say about the shape of the request it counts.
REQUEST_TYPES = {"", "read", "write", "delete", "any"}

#: The resources a migration reads most, one per spending hierarchy.
SPENDING_TYPES = (
    DriveItem,  # and everything else on ``BaseItem``
    Drive,
    Permission,
    ChatMessage,
    MailFolder,
    Calendar,
    Subscription,
    SubscriptionCollection,
    OnenotePage,
    Invitation,
    ConditionalAccessPolicy,
)


def _response(status_code: int = 200, headers: dict | None = None, body: bytes = b"{}") -> Response:
    response = Response()
    response.status_code = status_code
    response.url = "https://contoso.sharepoint.com/_api/web"
    response.headers.update(headers or {})
    response._content = body
    return response


def _make_exception(status_code: int, headers: dict | None = None) -> ClientRequestException:
    return ClientRequestException.from_response(
        _response(status_code, headers, b'{"error":{"code":"-1, System.Exception","message":"boom"}}')
    )


# --- what is transient ---------------------------------------------------------------


def test_a_permanent_failure_is_not_retried():
    # An unparseable URL cannot heal, so a retry only multiplies the same failure.
    func = mock.Mock(side_effect=requests.exceptions.InvalidURL("nope"))
    with mock.patch("office365.runtime.retry.sleep") as sleep_mock, pytest.raises(requests.exceptions.InvalidURL):
        retry(func, max_retry=5, timeout_secs=1)

    assert func.call_count == 1
    sleep_mock.assert_not_called()


def test_only_connection_failures_are_transient():
    transient = [
        requests.ConnectionError("boom"),
        requests.Timeout("slow"),
        requests.exceptions.ChunkedEncodingError("cut"),
    ]
    permanent = [requests.exceptions.SSLError("bad cert"), requests.exceptions.InvalidURL("nope")]
    assert all(is_transient_error(err) for err in transient)
    assert not any(is_transient_error(err) for err in permanent)
    # A reset is for a broken connection, not for a refusal: a 429 is answered, not dropped.
    assert should_reset_connections(_make_exception(503))
    assert should_reset_connections(requests.ConnectionError("boom"))
    assert not should_reset_connections(_make_exception(429))
    assert not should_reset_connections(_make_exception(400))
    assert not should_reset_connections(requests.exceptions.SSLError("bad cert"))


# --- how long to wait ----------------------------------------------------------------


def test_exponential_growth_and_its_jitter():
    assert backoff_delay(1, base=5, jitter=False) == 5  # noqa: PLR2004
    assert backoff_delay(2, base=5, jitter=False) == 10  # noqa: PLR2004
    assert backoff_delay(3, base=5, jitter=False) == 20  # noqa: PLR2004
    for attempt in (1, 2, 3):  # noqa: PLR2004
        nominal = backoff_delay(attempt, base=5, jitter=False)
        for _ in range(50):  # noqa: PLR2004
            assert 0 <= backoff_delay(attempt, base=5) <= nominal


def test_retry_after_is_read_as_a_date_or_bounded_by_the_caller():
    future = datetime.now(timezone.utc) + timedelta(seconds=30)
    dated = _response(503, {"Retry-After": format_datetime(future, usegmt=True)})
    assert 28 <= response_retry_after(dated) <= 30  # noqa: PLR2004
    # A caller who names a ceiling keeps it, whatever ``Retry-After`` says.
    func = mock.Mock(side_effect=[_make_exception(429, {"Retry-After": "600"}), None])
    with mock.patch("office365.runtime.retry.sleep") as sleep_mock:
        retry(func, max_retry=5, max_delay=30)
    sleep_mock.assert_called_once_with(30)


# --- how long the limiter holds the door shut ----------------------------------------


class _FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


def _limiter(per_scope: bool = False) -> tuple[RateLimiter, list[float], _FakeClock]:
    clock = _FakeClock()
    slept: list[float] = []

    def _sleep(delay: float) -> None:
        slept.append(delay)
        clock.t += delay

    return RateLimiter(per_scope=per_scope, clock=clock, sleep=_sleep), slept, clock


def test_retry_after_gates_the_group():
    limiter, slept, _clock = _limiter()
    limiter.observe(_response(429, {"Retry-After": "1"}))
    limiter.acquire()
    assert sum(slept) == pytest.approx(1.0)


def test_a_scope_signal_names_the_scope_that_was_throttled():
    limiter, _slept, _clock = _limiter()
    limiter.observe(_response(429, {"Retry-After": "5", "x-ms-throttle-scope": "Mail.ReadWrite"}))
    assert limiter.snapshot().next_available_at >= 5.0  # noqa: PLR2004
    assert limiter.last_scope == "Mail.ReadWrite"


def test_per_scope_isolates_the_throttled_scope():
    limiter, slept, _clock = _limiter(per_scope=True)
    limiter.observe(_response(429, {"Retry-After": "5", "x-ms-throttle-scope": "Mail.ReadWrite"}))

    # The global gate is untouched, so an unrelated scope is not made to wait.
    assert limiter.snapshot().next_available_at == 0.0
    limiter.acquire("Files.Read")
    assert slept == []
    assert limiter.snapshot("Mail.ReadWrite").next_available_at == 5.0  # noqa: PLR2004
    limiter.acquire("Mail.ReadWrite")
    assert sum(slept) >= 5.0  # noqa: PLR2004

    limiter.reset()
    assert limiter.snapshot("Mail.ReadWrite").next_available_at == 0.0
    assert limiter.last_scope is None


# --- what the headers say ------------------------------------------------------------


def test_a_throttling_header_is_read_in_its_own_units():
    malformed = parse_throttling(_response(headers={"RateLimit-Remaining": "abc", "RateLimit-Reset": "30"}))
    assert malformed == ThrottleLimits(remaining=None, reset=30, status=200)

    graph = parse_throttling(
        _response(
            headers={
                "Retry-After": "10",
                "x-ms-throttle-limit-percentage": "1.2",
                "x-ms-resource-unit": "3",
                "x-ms-throttle-scope": "Tenant_Application/ReadWrite/app/tenant",
                "x-ms-throttle-information": "WriteLimitExceeded",
            }
        )
    )
    assert graph is not None
    assert graph.retry_after == 10  # noqa: PLR2004
    assert graph.limit_percentage == 1.2  # noqa: PLR2004
    assert graph.resource_unit == 3  # noqa: PLR2004
    assert graph.scope == "Tenant_Application/ReadWrite/app/tenant"
    assert graph.reason == "WriteLimitExceeded"


def test_pacing_follows_the_limit_percentage():
    now = 1000.0
    assert pace(PaceState(), ThrottleLimits(limit_percentage=1.2), now=now).next_available_at > now
    assert pace(PaceState(), ThrottleLimits(limit_percentage=0.5), now=now) == PaceState()


def test_the_guard_attaches_and_detaches():
    from office365.graph_client import GraphClient

    client = GraphClient()
    seen = []
    with throttle_guard(client, on_limits=seen.append):
        client.pending_request().afterExecute(_response(headers={"RateLimit-Remaining": "7", "RateLimit-Reset": "10"}))
        assert len(seen) == 1
        assert seen[0].remaining == 7  # noqa: PLR2004
    # The hook is detached on exit: firing it again does nothing.
    client.pending_request().afterExecute(_response(headers={"RateLimit-Remaining": "1"}))
    assert len(seen) == 1


def test_a_priority_is_a_word_the_client_accepts_named():
    from office365.graph_client import GraphClient

    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.with_throttle_priority("high")
    request = RequestOptions(url="https://graph.microsoft.com/v1.0/me")
    client.pending_request().beforeExecute(request)
    assert request.headers.get("x-ms-throttle-priority") == "high"
    with pytest.raises(ValueError, match="priority"):
        GraphClient().with_throttle_priority("urgent")


# --- what a ceiling is ---------------------------------------------------------------

_ROOT_ROWS = (
    Limit("microsoft teams", 200, LimitKind.SUPPORTED, "requests", "app", doc="https://example.com", window_seconds=1),
    Limit(
        "microsoft teams",
        1,
        LimitKind.SUPPORTED,
        "requests",
        "user",
        doc="https://example.com",
        window_seconds=1,
        request_type="write",
    ),
)


class _NavigationOutermost(ClientObject):
    """``@odata`` above ``@limit``: two facts, two decorators, one member."""

    @odata(name="channels", navigation=True)
    @property
    @limit(*_ROOT_ROWS)
    def channels(self) -> object:
        """The channel collection."""


class _NavigationInnermost(ClientObject):
    """The other order, because nothing but ``TypeSchema`` reads a marker."""

    @limit(*_ROOT_ROWS)
    @odata(name="channels", navigation=True)
    @property
    def channels(self) -> object:
        """The channel collection."""


def test_every_published_row_is_well_formed():
    rows = catalog()
    assert rows, "no rows registered - the catalogs registered nothing at all"
    assert "graph" in catalog_products(), "the Graph-wide row is the one every request spends"
    for row in rows:
        assert row.name
        assert isinstance(row.kind, LimitKind)
        assert row.value > 0
        assert row.unit, f"{row.name!r} counts an unnamed unit"
        assert row.request_type in REQUEST_TYPES
        assert (row.window_seconds or 0) >= 0
        assert row.doc.startswith("https://"), f"{row.name!r} cites {row.doc!r}"


def test_one_import_exposes_every_catalog():
    # A product catalog registers itself when imported, so the aggregator has to import all of
    # them; a new ``quotas`` module nobody adds there would answer ``[]`` for its product.
    code = """
import importlib, pkgutil
import office365
from office365.limits import catalog_products

seen = set(catalog_products())
for module in pkgutil.walk_packages(office365.__path__, "office365."):
    if module.name.endswith((".quotas", ".thresholds")):
        importlib.import_module(module.name)
print(sorted(set(catalog_products()) - seen - {"model"}))  # "model" is written by @limit on a class
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "[]", f"not imported by office365/limits.py: {result.stdout.strip()}"


@pytest.mark.parametrize("target", SPENDING_TYPES, ids=lambda target: target.__name__)
def test_a_type_answers_the_rows_it_spends(target):
    declared = limits_of(target)
    assert declared, f"{target.__name__} declares no limits"
    for decl in declared:
        assert decl.limit in catalog(), f"{target.__name__} declares a row no catalog published"


def test_a_row_reads_as_a_budget():
    assert str(LIST_VIEW) == "5,000 items"
    assert str(Limits.FILE_UPLOAD) == "250 GB"
    assert str(Limits.LIST_ROW_BYTES) == "8,000 bytes"
    # A byte budget inside a window is bytes, not a count, however it is spent.
    assert str(Limit("upload", 150 * 1024 * 1024, LimitKind.SUPPORTED, "bytes", window_seconds=300)) == "150 MB / 300s"
    # A whole-day allocation stated in seconds must not read like a per-second rate.
    assert str(Limit("queries", 200, LimitKind.THRESHOLD, "requests", window_seconds=86_400)) == "200 requests / 24h"
    assert str(Limit("upload", 100 * 1024**3, LimitKind.THRESHOLD, "bytes", window_seconds=3600)) == "100 GB / 1h"


@pytest.mark.parametrize("offset", [-1, 0])
def test_the_guard_accepts_a_value_at_the_boundary(offset):
    value = LIST_VIEW.value + offset
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert not warn_if_exceeds(LIST_VIEW, value)
        ensure_within(LIST_VIEW, value)


def test_the_guard_stops_at_the_first_value_above_the_boundary():
    value = LIST_VIEW.value + 1
    with pytest.warns(UserWarning, match="list view threshold"):
        assert warn_if_exceeds(LIST_VIEW, value)
    with pytest.raises(LimitExceededError) as error:
        ensure_within(LIST_VIEW, value)
    assert error.value.value == value


def test_ensure_within_raises_warns_or_passes():
    with pytest.raises(LimitExceededError) as exc:
        ensure_within(LIST_VIEW, 9000, context="query")
    assert exc.value.limit is LIST_VIEW
    assert exc.value.value == 9000  # noqa: PLR2004
    assert "query" in str(exc.value)
    with pytest.warns(UserWarning):
        ensure_within(LIST_VIEW, 9000, on_exceed="warn")
    ensure_within(LIST_VIEW, 10)  # under the limit -> no raise, no warning
    with pytest.raises(ValueError, match="on_exceed"):
        ensure_within(LIST_VIEW, 10, on_exceed="nope")


def test_bounded_warns_and_lets_the_call_through():
    @bounded("page_size", LIST_VIEW)
    def get_items(caml_query=None, page_size=None):
        return page_size

    with pytest.warns(UserWarning):
        assert get_items(page_size=6000) == 6000  # noqa: PLR2004
    assert get_items(page_size=2000) == 2000  # noqa: PLR2004
    assert get_items() is None  # None passes


def test_the_list_get_items_ceiling_is_the_published_one():
    lst = ClientContext(test_site_url).web.lists.get_by_title("X")
    with pytest.warns(UserWarning, match="list view threshold"):
        lst.get_items(page_size=LIST_VIEW_THRESHOLD + 1)


def test_the_decorator_stamps_metadata_and_doc():
    @limit(Limits.FILE_UPLOAD)
    def upload(content):
        """Upload a file."""
        return content

    decls = limits_of(upload)
    assert len(decls) == 1
    assert decls[0].limit is Limits.FILE_UPLOAD
    assert decls[0].arg is None
    assert "Limits:" in upload.__doc__
    assert "file upload" in upload.__doc__


def test_the_decorator_can_raise_or_clamp():
    @limit(Limits.LIST_VIEW, arg="page_size", on_exceed="raise")
    def strict(page_size=None):
        return page_size

    with pytest.raises(LimitExceededError):
        strict(page_size=6000)

    @limit(Limits.LIST_VIEW, arg="page_size", clamp=True)
    def clamped(page_size=None):
        return page_size

    assert clamped(page_size=6000) == Limits.LIST_VIEW.value  # noqa: PLR2004


def test_limits_are_one_of_the_things_a_type_declares():
    # A class's limits and its slots are the same kind of fact, so they live together.

    @limit(Limits.LIST_VIEW)
    class _Tier(ClientObject):
        @limit(Limits.FILE_UPLOAD)
        @property
        def upload(self):
            return None

        @limit(Limits.BATCH_ITEMS, arg="page_size")
        def get_items(self, page_size=None):
            return page_size

    class _Child(_Tier):
        pass

    assert [decl.limit for decl in _Tier._schema.class_limits] == [Limits.LIST_VIEW]
    assert set(_Tier._schema.member_limits) == {"upload", "get_items"}
    assert _Tier.declared_limits() == (Limits.LIST_VIEW, Limits.FILE_UPLOAD, Limits.BATCH_ITEMS)
    # The type's own row comes first: a class is subject to what it declares on itself.
    assert [decl.limit for decl in limits_of(_Tier)] == [Limits.LIST_VIEW, Limits.FILE_UPLOAD, Limits.BATCH_ITEMS]
    assert _Child._schema.class_limits == _Tier._schema.class_limits  # inherited, not a shared map
    assert _Child._schema is not _Tier._schema
    assert Limits.LIST_VIEW in _Child.declared_limits()
    # A context declares no properties, and still declares limits.
    assert ClientContext._schema.properties == {}
    assert Limits.BATCH_ITEMS in ClientContext.declared_limits()


def test_a_row_declared_by_two_members_is_one_ceiling():
    # Asking the class used to answer only the members' rows, so ``verify_limits`` said
    # "0 limit(s)" for a type whose rows were written on the class itself.

    @limit(Limits.LIST_VIEW)
    class _Tier(ClientObject):
        @limit(Limits.BATCH_ITEMS, arg="items_per_batch")
        def execute_batch(self, items_per_batch=None):
            return items_per_batch

        @limit(Limits.BATCH_ITEMS, arg="items_per_batch")
        def execute_batch_async(self, items_per_batch=None):
            return items_per_batch

    report = verify_limits(_Tier)
    assert report.limits == (Limits.LIST_VIEW, Limits.BATCH_ITEMS)
    assert [decl.limit for decl in limits_of(_Tier)] == [Limits.LIST_VIEW, Limits.BATCH_ITEMS]


def test_a_violation_is_reported_against_the_row_it_broke():
    @limit(Limits.LIST_VIEW, arg="page_size")
    def get_items(page_size=None):
        return page_size

    assert verify_limits(get_items, page_size=10).ok
    report = verify_limits(get_items, page_size=6000)
    assert not report.ok
    assert "list view threshold" in str(report)


# --- the list view threshold ----------------------------------------------------------


def _query(column: str = "Status", *, paged: bool = False) -> CamlQuery:
    builder = CamlQuery.builder().where(Caml.text(column).eq("Active"))
    return (builder.row_limit(500) if paged else builder).build()


def _large() -> int:
    return LIST_VIEW_THRESHOLD * 2


def test_a_list_at_the_threshold_is_not_warned_about():
    assert threshold_warnings(_query(), item_count=LIST_VIEW_THRESHOLD) == []


def test_a_paged_query_is_never_warned_about():
    assert threshold_warnings(_query(paged=True), item_count=_large()) == []


def test_an_unpaged_query_over_a_large_list_names_the_column_to_index():
    (warning,) = threshold_warnings(_query(), item_count=_large())
    assert "'Status'" in warning, "the warning names the column the query filters on"
    assert "ensure_indexed('Status')" in warning, "and how to fix it"
    assert "page_size=" in warning, "or the paging argument that sidesteps it"
    with pytest.warns(UserWarning, match="list view threshold"):
        warn_if_unpaged(_query(), item_count=_large())


def test_an_unpaged_query_with_no_columns_and_unknown_size_is_silent():
    # ``create_all_items_query`` reads everything anyway; there is nothing to index.
    assert threshold_warnings(CamlQuery.create_all_items_query()) == []


class _ThresholdCollection(ClientObjectCollection):
    _list_view_threshold = 3
    _truncation_hint = "page it"


def test_a_load_that_fills_the_threshold_warns_once_however_many_rows_arrive():
    collection = _ThresholdCollection(offline_sharepoint_context(), Field, ResourcePath("x"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for _ in range(_ThresholdCollection._list_view_threshold + 2):
            collection.add_child(Field(collection.context))
    (warning,) = [w for w in caught if issubclass(w.category, UserWarning)]
    assert "page it" in str(warning.message)


# --- what a failure says -------------------------------------------------------------

#: The Intune proxy wraps ``error.message`` in a JSON object.
INTUNE_MESSAGE = json.dumps({"_version": 3, "Message": "Application is not authorized to perform this operation."})

#: Some services append support diagnostics to an otherwise plain message.
SUPPORT_TAIL = " - Operation ID (for customer support): 00000000-0000-0000-0000-000000000000"

#: A shared lock, as SharePoint spells it: the HRESULT first, then the .NET type.
LOCKED_BODY = (
    b'{"error":{"code":"-2147018894, Microsoft.SharePoint.SPFileLockException",'
    b'"message":"The file report.xlsx is locked for shared use by John Doe [membership]."}}'
)


def _error_response(body: dict | bytes, status: int = 400, headers: dict | None = None) -> Response:
    raw = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
    return _response(status, headers, raw)


def test_a_malformed_body_is_a_request_exception_not_a_value_error():
    ctx = ClientContext(test_site_url)
    request = ODataRequest(test_site_url, JsonLightFormat())
    query = ClientQuery(ctx, return_type=ClientResult(ctx))
    resp = _error_response(b"<html><body>Expired form digest</body></html>", status=200)
    resp.headers["Content-Type"] = "application/json"
    with pytest.raises(ClientRequestException) as caught:
        request.handle_response(resp, query)
    assert caught.value.response is resp


def test_a_proxy_message_is_unwrapped_to_its_inner_text():
    assert _clean_message(INTUNE_MESSAGE) == "Application is not authorized to perform this operation."
    inner = (
        "Application is not authorized to perform this operation. "
        "Application must have one of the following scopes: DeviceManagementApps.Read.All"
    )
    noisy = inner + " - Operation ID (for customer support): 0000 - Activity ID: abc - Url: https://proxy"
    exc = ClientRequestException.from_response(
        _error_response({"error": {"code": "Forbidden", "message": json.dumps({"_version": 3, "Message": noisy})}})
    )
    assert exc.message == inner
    assert inner in str(exc)
    assert "_version" not in str(exc)
    assert "Activity ID" not in str(exc)


def test_a_support_tail_is_dropped_from_a_plain_message():
    assert _clean_message("Access denied." + SUPPORT_TAIL) == "Access denied."
    assert _clean_message("Access denied.") == "Access denied."


def test_a_sharepoint_code_splits_into_an_hresult_and_a_type_name():
    payload = ErrorPayload(code="-2147018894, Microsoft.SharePoint.SPFileLockException")
    assert payload.hresult == "-2147018894"
    assert payload.error_type == "Microsoft.SharePoint.SPFileLockException"
    # A symbolic Graph code has neither: splitting it would invent an HRESULT.
    symbolic = ErrorPayload(code="Authorization_RequestDenied")
    assert symbolic.hresult is None
    assert symbolic.error_type is None


def test_a_locked_file_arrives_as_the_lock_exception_and_names_its_owner():
    failed = ClientRequestException.from_response(_error_response(LOCKED_BODY, status=423))
    assert isinstance(failed, FileLockedException)
    assert "John Doe" in str(failed)
    assert "shared lock" in str(failed)


def test_a_throttled_query_names_the_threshold():
    exc = ClientRequestException.from_response(
        _error_response(
            {
                "error": {
                    "code": "-2147024860, Microsoft.SharePoint.SPQueryThrottledException",
                    "message": {
                        "lang": "en-US",
                        "value": "The attempted operation is prohibited because it exceeds the list view threshold.",
                    },
                }
            }
        )
    )
    assert isinstance(exc, SPQueryThrottledException)
    assert "list view threshold" in str(exc).lower()


def test_a_hint_is_rendered_below_the_message_and_a_blank_one_is_ignored():
    failed = ClientRequestException("Access denied.").add_hint("").add_hint("Requires Sites.Read.All.")
    assert failed.hints == ("Requires Sites.Read.All.",)
    assert str(failed).splitlines() == ["Access denied.", "Requires Sites.Read.All."]


def test_a_failure_exposes_the_diagnostics_it_was_given():
    graph = ClientRequestException.from_response(
        _error_response(
            {
                "error": {
                    "code": "TooManyRequests",
                    "message": "Please retry again later.",
                    "innerError": {
                        "code": "429",
                        "request-id": "94fb3b52-452a-4535-a601-69e0a90e3aa2",
                        "status": "429",
                    },
                }
            }
        )
    )
    assert graph.request_id == "94fb3b52-452a-4535-a601-69e0a90e3aa2"
    assert graph.inner_error is not None
    assert graph.inner_error["status"] == "429"

    sharepoint = ClientRequestException.from_response(
        _error_response(
            {"error": {"code": "-1, System.Exception", "message": "boom"}},
            headers={
                "SPRequestGuid": "a1b2c3d4-1234-5678-9abc-def012345678",
                "SPRequestDuration": "127",
                "X-SharePointHealthScore": "3",
            },
        )
    )
    assert sharepoint.server_guid == "a1b2c3d4-1234-5678-9abc-def012345678"
    assert sharepoint.duration_ms == 127  # noqa: PLR2004
    assert sharepoint.health_score == 3  # noqa: PLR2004

    # A service that names none of it answers ``None``, never a guess.
    bare = ClientRequestException.from_response(_error_response({"error": {"message": "boom"}}))
    assert bare.request_id is None
    assert bare.inner_error is None
    assert bare.server_guid is None
    assert bare.duration_ms is None
    assert bare.health_score is None


# --- what a progress report carries ---------------------------------------------------


def test_a_report_carries_the_total_it_was_given():
    seen = []
    tracker = ProgressTracker(seen.append, total=10, stage="uploading")
    tracker.report(3)
    tracker.report(5)
    assert [report.done for report in seen] == [3, 5]
    assert all(report.total == 10 for report in seen)  # noqa: PLR2004
    assert all(report.stage == "uploading" for report in seen)


def test_a_late_total_still_prices_the_work_already_done():
    seen = []
    tracker = ProgressTracker(seen.append, stage="migrating")
    tracker.advance()
    tracker.advance(2)
    tracker.set_total(10)
    tracker.report(5)
    assert [report.done for report in seen] == [1, 3, 5]
    assert seen[-1].total == 10  # noqa: PLR2004
    assert seen[-1].percent == 50.0  # noqa: PLR2004


def test_advances_from_many_threads_sum_to_the_total():
    seen = []
    tracker = ProgressTracker(seen.append, total=1000, stage="parallel")
    threads = [threading.Thread(target=lambda: [tracker.advance() for _ in range(100)]) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert tracker.done == 1000  # noqa: PLR2004
    assert len(seen) == 1000  # noqa: PLR2004
