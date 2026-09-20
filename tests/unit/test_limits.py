"""Unit tests for the service-limit catalog and guard-rails."""

from __future__ import annotations

import warnings

import pytest
from office365.runtime.limits import (
    Limit,
    LimitExceededError,
    LimitKind,
    bounded,
    ensure_within,
    exceeds,
    hint,
    warn_if_exceeds,
)
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD, SAFE_PAGE_SIZE, Limits

LIST_VIEW = Limits.LIST_VIEW


def test_catalog_is_populated_and_well_formed():
    catalog = Limits.catalog()
    assert len(catalog) >= 30  # noqa: PLR2004
    names = [limit.name for limit in catalog]
    assert len(names) == len(set(names))  # unique names
    for limit in catalog:
        assert isinstance(limit, Limit)
        assert isinstance(limit.kind, LimitKind)
        assert limit.value > 0
        assert limit.unit


def test_list_view_threshold_constant_matches_catalog():
    assert LIST_VIEW_THRESHOLD == LIST_VIEW.value
    assert SAFE_PAGE_SIZE < LIST_VIEW_THRESHOLD


def test_str_formats_items_and_bytes():
    assert str(LIST_VIEW) == "5,000 items"
    assert str(Limits.FILE_UPLOAD) == "250 GB"
    assert str(Limits.LIST_ROW_BYTES) == "8,000 bytes"


def test_exceeds():
    assert exceeds(LIST_VIEW, LIST_VIEW.value + 1) is True
    assert exceeds(LIST_VIEW, LIST_VIEW.value) is False


def test_warn_if_exceeds():
    with pytest.warns(UserWarning, match="list view threshold"):
        assert warn_if_exceeds(LIST_VIEW, 6000) is True
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert warn_if_exceeds(LIST_VIEW, 10) is False


def test_ensure_within_raises_by_default():
    with pytest.raises(LimitExceededError) as exc:
        ensure_within(LIST_VIEW, 9000, context="query")
    assert exc.value.limit is LIST_VIEW
    assert exc.value.value == 9000  # noqa: PLR2004
    assert "query" in str(exc.value)


def test_ensure_within_warn_mode_and_passthrough():
    with pytest.warns(UserWarning):
        ensure_within(LIST_VIEW, 9000, on_exceed="warn")
    ensure_within(LIST_VIEW, 10)  # under the limit -> no raise
    with pytest.raises(ValueError, match="on_exceed"):
        ensure_within(LIST_VIEW, 10, on_exceed="nope")


def test_hint_includes_context_and_docs():
    text = hint(LIST_VIEW, context="get_items", value=6000)
    assert "get_items" in text
    assert "6,000 items" in text
    assert "learn.microsoft.com" in text


def test_bounded_warns_by_default():
    @bounded("page_size", LIST_VIEW)
    def get_items(caml_query=None, page_size=None):
        return page_size

    with pytest.warns(UserWarning):
        assert get_items(page_size=6000) == 6000  # noqa: PLR2004
    assert get_items(page_size=2000) == 2000  # noqa: PLR2004
    assert get_items() is None  # None passes


def test_bounded_clamps_and_handles_positional_args():
    @bounded("page_size", LIST_VIEW, clamp=True)
    def get_items(caml_query, page_size):
        return page_size

    assert get_items(None, 6000) == LIST_VIEW.value
    assert get_items(None, 100) == 100  # noqa: PLR2004


def test_bounded_raise_mode_and_validation():
    @bounded("page_size", LIST_VIEW, on_exceed="raise")
    def get_items(page_size=None):
        return page_size

    with pytest.raises(LimitExceededError):
        get_items(page_size=6000)
    with pytest.raises(ValueError, match="on_exceed"):
        bounded("page_size", LIST_VIEW, on_exceed="nope")
