"""Offline tests for ``ListItem.set_system_metadata``.

What a live run cannot show is the *shape* of the request: which field names a form
value carries, the ``...Z`` form ``datesInUTC`` requires, and that every value rides in
one write. Each assertion below is a wire fact the tenant would only report as a silent
"the value did not change".
"""

from __future__ import annotations

import datetime

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from tests import test_site_url
from tests._scripted_transport import RecordingTransport


def _sp(payloads):
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    transport = RecordingTransport(payloads)
    ctx.pending_request().transport = transport
    return ctx, transport


def _item(ctx):
    return ctx.web.lists.get_by_title("Documents").get_item_by_id(1)


def _sent(transport) -> dict:
    """The body as the transport receives it: a form value is serialized by its own class."""
    return transport.requests[0].data


def _form_values(body: dict) -> dict:
    return {value["FieldName"]: value["FieldValue"] for value in body["formValues"]}


def _accepted() -> dict:
    return {"d": {"ValidateUpdateListItem": {"results": [{"FieldName": "Created", "HasException": False}]}}}


def test_every_value_rides_in_one_request():
    """A second write would re-approve the item, so timestamps and authorship go together."""
    ctx, transport = _sp([_accepted()])

    _item(ctx).set_system_metadata(
        {
            "Created": datetime.datetime(2020, 1, 2, 3, 4, 5),
            "Modified": datetime.datetime(2021, 6, 7, 8, 9, 10, tzinfo=datetime.timezone.utc),
            "Author": FieldLookupValue(12, "i:0#.f|membership|author@contoso.com"),
        },
        new_document_update=True,
    ).execute_query()

    assert len(transport.requests) == 1
    body = _sent(transport)
    assert body["datesInUTC"] is True
    assert body["bNewDocumentUpdate"] is True
    assert _form_values(body) == {
        "Created": "2020-01-02T03:04:05Z",
        "Modified": "2021-06-07T08:09:10Z",
        "Author": "[{'Key':'i:0#.f|membership|author@contoso.com'}]",
    }


def test_a_string_value_is_sent_as_given():
    """A document's form dates are read in the web's locale, so a converted wall clock
    must reach the service exactly as the conversion returned it."""
    ctx, transport = _sp([_accepted()])

    _item(ctx).set_system_metadata({"Created": "2020-01-02T05:04:05"}, new_document_update=True).execute_query()

    assert _form_values(_sent(transport)) == {"Created": "2020-01-02T05:04:05"}


def test_a_user_value_becomes_its_lookup_value():
    """A resolved principal is passed as a model object; the wire takes its login."""
    ctx, transport = _sp([_accepted()])
    author = ctx.web.site_users.get_by_id("12")
    author.set_property("Id", 12)
    author.set_property("LoginName", "i:0#.f|membership|author@contoso.com")

    _item(ctx).set_system_metadata({"Author": author}, new_document_update=True).execute_query()

    assert _form_values(_sent(transport)) == {"Author": "[{'Key':'i:0#.f|membership|author@contoso.com'}]"}


def test_a_moderation_column_is_written_without_its_escape_prefix():
    """The model declares ``OData__ModerationStatus``; the write takes the internal name."""
    ctx, transport = _sp([_accepted()])

    _item(ctx).set_system_metadata({"OData__ModerationStatus": 0}, new_document_update=True).execute_query()

    assert _form_values(_sent(transport)) == {"_ModerationStatus": "0"}


def test_nothing_to_write_queues_no_request():
    ctx, transport = _sp([])

    result = _item(ctx).set_system_metadata({"Created": None}).execute_query()

    assert transport.requests == []
    assert list(result.value or []) == []


def test_a_rejection_is_visible_on_the_result():
    """The caller reports it; the verb does not swallow a field the service refused."""
    ctx, _ = _sp(
        [
            {
                "d": {
                    "ValidateUpdateListItem": {
                        "results": [
                            {
                                "FieldName": "Author",
                                "HasException": True,
                                "ErrorMessage": "The user does not exist.",
                            }
                        ]
                    }
                }
            }
        ]
    )

    result = _item(ctx).set_system_metadata({"Author": FieldLookupValue(12, "nobody")}).execute_query()

    rejected = [value for value in result.value if value.HasException]
    assert [(value.FieldName, value.ErrorMessage) for value in rejected] == [("Author", "The user does not exist.")]
