"""Unit tests for the Microsoft Graph throttling-limit catalog."""

from __future__ import annotations

from office365.graph_limits import GraphLimits
from office365.runtime.limits import Limit


def test_catalog_is_populated_and_well_formed():
    catalog = GraphLimits.catalog()
    assert len(catalog) >= 20  # noqa: PLR2004
    for entry in catalog:
        assert isinstance(entry, Limit)
        assert entry.name
        assert entry.value >= 0
        assert entry.window_seconds is not None  # rate quotas
        assert entry.scope in {"app", "tenant", "app+tenant", "resource", "user"}
        assert entry.request_type in {"any", "read", "write"}
        assert entry.unit in {"requests", "resource_units", "concurrent"}
        assert entry.doc


def test_global_limit():
    assert GraphLimits.GLOBAL.value == 130_000  # noqa: PLR2004
    assert GraphLimits.GLOBAL.window_seconds == 10  # noqa: PLR2004
    assert GraphLimits.GLOBAL.scope == "app"
    assert GraphLimits.GLOBAL.is_rate


def test_str_formats_rate_and_concurrency():
    assert str(GraphLimits.GLOBAL) == "130,000 requests / 10s"
    assert str(GraphLimits.BOOKINGS) == "4 concurrent"


def test_identity_uses_resource_units():
    assert GraphLimits.IDENTITY_APP.unit == "resource_units"
    assert GraphLimits.IDENTITY_WRITE.request_type == "write"


def test_graph_client_binds_identity_quotas():
    from office365.graph_client import GraphClient

    assert "users" in GraphClient._limit_meta
    assert "groups" in GraphClient._limit_meta
    assert "applications" in GraphClient._limit_meta
    assert GraphLimits.IDENTITY in GraphClient.declared_limits()
