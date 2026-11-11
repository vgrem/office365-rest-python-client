"""Offline tests for declarative OData query-option capabilities.

Covers the ``@query_capabilities`` declaration, its collection into the model,
and the guard the ``ClientObjectCollection`` fluent setters apply — including the
``callRecords`` feed, which rejects ``$top``.
"""

from __future__ import annotations

import pytest
from office365.communications.callrecords.collection import CallRecordCollection
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.onedrive.driveitems.collection import DriveItemCollection
from office365.runtime.http.prefer import TRY_FILTER_LAST_MODIFIED_DATE_TIME
from office365.runtime.query_capabilities import (
    QueryOptionNotSupportedError,
    QueryPropertyNotSupportedError,
    query_capabilities,
    query_capabilities_of,
)
from office365.security.labels.retention.collection import RetentionLabelCollection
from office365.security.triggertypes.collection import RetentionEventTypeCollection
from tests._scripted_transport import RecordingTransport, graph


def test_call_records_declares_top_unsupported():
    capability = query_capabilities_of(CallRecordCollection)
    assert capability is not None
    assert capability.supports("filter")
    assert not capability.supports("top")
    assert not capability.supports("$Top")  # normalized


def test_retention_feeds_refuse_every_standard_option():
    """Both Purview retention feeds answer 400 to each option, so the guard runs before the request.

    Measured against the two endpoints rather than inferred: the bare GET is the only request
    those feeds accept, and it is gated by Purview RBAC, which is why no live test can see this.
    """
    event_types = RetentionEventTypeCollection(GraphClient())
    labels = RetentionLabelCollection(GraphClient())
    for collection in (event_types, labels):
        with pytest.raises(QueryOptionNotSupportedError) as error:
            collection.top(3)
        assert "learn.microsoft.com" in str(error.value)
        with pytest.raises(QueryOptionNotSupportedError):
            collection.filter("displayName eq 'x'")


def test_paged_and_get_all_are_guarded():
    records = GraphClient().communications.call_records
    with pytest.raises(QueryOptionNotSupportedError):
        records.paged(20)
    with pytest.raises(QueryOptionNotSupportedError):
        records.get_all(page_size=20)


@query_capabilities(allowed={"filter", "select"})
class _FilterSelectOnly(EntityCollection):
    pass


def test_allow_list_guards_other_options():
    col = _FilterSelectOnly(GraphClient(), Entity)
    col.filter("id eq '1'")
    col.select(["id"])
    with pytest.raises(QueryOptionNotSupportedError):
        col.top(1)
    with pytest.raises(QueryOptionNotSupportedError):
        col.order_by("id")


@query_capabilities(unsupported={"top"}, on_unsupported="warn")
class _WarnTop(EntityCollection):
    pass


def test_warn_mode_skips_the_option():
    col = _WarnTop(GraphClient(), Entity)
    with pytest.warns(UserWarning):
        col.top(5)
    assert col.query_options.top is None


def test_declaration_validation():
    with pytest.raises(ValueError):
        query_capabilities(unsupported={"top"}, allowed={"filter"})
    with pytest.raises(ValueError):
        query_capabilities(unsupported={"top"}, on_unsupported="nope")


# --- property-level capabilities -------------------------------------------------


def test_property_violation_warn_keeps_the_expression():
    @query_capabilities(unsupported_filter={"size"}, on_unsupported="warn")
    class _WarnProperty(EntityCollection):
        pass

    col = _WarnProperty(GraphClient(), Entity)
    with pytest.warns(UserWarning):
        col.filter("size gt 0")
    assert col.query_options.filter == "size gt 0"


def test_drive_item_capability():
    capability = query_capabilities_of(DriveItemCollection)
    assert capability is not None
    assert capability.filter_violations("size gt 0") == ("size",)
    assert capability.filter_violations("folder ne null") == ()
    assert capability.orderby_violations("size desc") == ()  # sorting by size is fine
    col = DriveItemCollection(GraphClient())
    with pytest.raises(QueryPropertyNotSupportedError):
        col.filter("size gt 0")
    col.order_by("size desc")  # allowed


def test_prefer_header_injected_for_last_modified_filter():
    transport = RecordingTransport([{"value": []}])
    client = graph(transport)[0]

    client.me.drive.root.children.filter("lastModifiedDateTime gt 2020-01-01T00:00:00Z").get().execute_query()

    prefer = transport.requests[-1].headers.get("Prefer", "")
    assert TRY_FILTER_LAST_MODIFIED_DATE_TIME in prefer
