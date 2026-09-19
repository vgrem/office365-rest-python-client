"""Unit tests for column indexing (list view threshold mitigation)."""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field import Field
from tests import test_site_url


def test_field_ensure_indexed_queues_update():
    ctx = ClientContext(test_site_url)
    field = Field(ctx)
    field.set_property("Indexed", False)

    field.ensure_indexed()

    assert field.properties["Indexed"] is True
    assert len(ctx._queries) == 1  # an update was queued


def test_field_ensure_indexed_is_idempotent():
    ctx = ClientContext(test_site_url)
    field = Field(ctx)
    field.set_property("Indexed", True)

    field.ensure_indexed()

    assert len(ctx._queries) == 0  # already indexed -> no update
