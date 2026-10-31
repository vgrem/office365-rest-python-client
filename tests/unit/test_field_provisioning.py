"""Offline tests for rich field provisioning.

``List.ensure_field`` / ``ensure_fields`` accept rich
:class:`FieldCreationInformation` specs (choices, formula, required, ...), and
``FieldCollection.ensure(..., on_conflict="update")`` reconciles those rich
settings on an existing column. Everything stays deferred — no request is sent
until ``execute_query()``.
"""

from __future__ import annotations

from office365.runtime.http.http_method import HttpMethod
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.creation_information import FieldCreationInformation
from office365.sharepoint.fields.type import FieldType
from tests import test_site_url
from tests._scripted_transport import RecordingTransport

_NOT_FOUND = {
    "http_status": 404,
    "body": {"error": {"code": "Request_ResourceNotFound", "message": "Resource not found"}},
}


def _sp(payloads):
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    transport = RecordingTransport(payloads)
    ctx.pending_request().transport = transport
    return ctx, transport


def _existing(**props):
    return {"d": props}


# --- declarative rich specs (deferred) ---------------------------------------


# --- rich reconcile on conflict ----------------------------------------------


def test_ensure_reconciles_choices_on_conflict_update():
    ctx, transport = _sp(
        [
            _existing(Title="Status", InternalName="Status", FieldTypeKind=6, Choices={"results": ["A", "B"]}),
            {},
        ]
    )

    field = (
        ctx.web.lists.get_by_title("Tasks")
        .fields.ensure(
            FieldCreationInformation(Title="Status", FieldTypeKind=FieldType.Choice, Choices=["A", "C"]),
            on_conflict="update",
        )
        .execute_query()
    )

    assert transport.calls == 2  # noqa: PLR2004
    assert list(field.choices) == ["A", "C"]
    # the reconcile patches the field entity itself, not the collection
    assert transport.requests[-1].method == HttpMethod.Post
    assert transport.requests[-1].headers.get("X-HTTP-Method") == "MERGE"
    assert transport.requests[-1].url.endswith("Fields/getByTitle('Status')")


def test_ensure_reconciles_formula_for_calculated():
    ctx, transport = _sp([_existing(Title="Total", FieldTypeKind=17, Formula="=1"), {}])

    field = (
        ctx.web.lists.get_by_title("Tasks")
        .fields.ensure(
            FieldCreationInformation(Title="Total", FieldTypeKind=FieldType.Calculated, Formula="=2"),
            on_conflict="update",
        )
        .execute_query()
    )

    assert transport.calls == 2  # noqa: PLR2004
    assert field.formula == "=2"


def test_ensure_turns_on_required():
    ctx, transport = _sp([_existing(Title="Owner", FieldTypeKind=2, Required=False), {}])

    field = (
        ctx.web.lists.get_by_title("Tasks")
        .fields.ensure(
            FieldCreationInformation(Title="Owner", FieldTypeKind=FieldType.Text, Required=True),
            on_conflict="update",
        )
        .execute_query()
    )

    assert transport.calls == 2  # noqa: PLR2004
    assert field.properties.get("Required") is True
