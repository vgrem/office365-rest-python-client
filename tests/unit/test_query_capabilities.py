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
from office365.runtime.query_capabilities import (
    QueryOptionNotSupportedError,
    query_capabilities,
    query_capabilities_of,
)


def test_call_records_declares_top_unsupported():
    capability = query_capabilities_of(CallRecordCollection)
    assert capability is not None
    assert capability.supports("filter")
    assert not capability.supports("top")
    assert not capability.supports("$Top")  # normalized


def test_call_records_top_raises():
    records = GraphClient().communications.call_records
    with pytest.raises(QueryOptionNotSupportedError) as err:
        records.top(20)
    assert "$top" in str(err.value)


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


def test_decorator_rejects_non_class():
    with pytest.raises(TypeError):
        query_capabilities(unsupported={"top"})(lambda: None)
