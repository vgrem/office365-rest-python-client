"""``to_json(CANONICAL)``: two spellings of one value share a form, a real change does not.

Each rule is a fact the service was measured to apply, declared on the field it is about
(``Compare``); these tests read it back through the one profile that applies them.
"""

from __future__ import annotations

import pytest
from office365.graph_client import GraphClient
from office365.migration.outlook import CalendarImportOptions
from office365.migration.outlook.calendar_models import EventRecord
from office365.outlook.calendar.attendees.attendee import Attendee
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.outlook.mail.location import Location
from office365.runtime.odata.canonical import CANONICAL
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.types.odata_property import Compare


def _contact(**payload) -> dict:
    return (
        Contact(GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"}))
        .hydrate({"displayName": "A", **payload}, V4JsonFormat())
        .to_json(CANONICAL)
    )


def _event(**payload) -> dict:
    return (
        Event(GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"}))
        .hydrate(payload, V4JsonFormat())
        .to_json(CANONICAL)
    )


def test_an_address_only_email_is_named_after_its_address():
    sent = _contact(emailAddresses=[{"address": "Bob@Contoso.com"}])
    read_back = _contact(emailAddresses=[{"address": "bob@contoso.com", "name": "bob@contoso.com"}])
    assert sent == read_back


def test_a_different_address_is_a_different_value():
    assert _contact(emailAddresses=[{"address": "a@x.com"}]) != _contact(emailAddresses=[{"address": "b@x.com"}])


def test_the_comparable_form_is_not_a_request():
    # A rule may synthesize what the sender never wrote -- ``fallback`` names a sibling,
    # ``default`` names a value -- because a digest is of the meaning. A body that leaves
    # the process may not: an import sends the person as stated, not as compared.
    envelope = {
        "subject": "S",
        "start": {"dateTime": "2026-03-02T09:00:00.0000000", "timeZone": "UTC"},
        "end": {"dateTime": "2026-03-02T10:00:00.0000000", "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": "Bob@Contoso.com"}, "type": "required"}],
    }
    options = CalendarImportOptions(restore_attendees=True)
    assert EventRecord.from_json(envelope).payload(options)["attendees"] == [
        {"emailAddress": {"address": "Bob@Contoso.com"}, "type": "required"}
    ]
    assert EventRecord.from_json(envelope).canonical(options)["attendees"] == [
        {"emailAddress": {"address": "bob@contoso.com", "name": "bob@contoso.com"}, "type": "required"}
    ]


def test_an_entry_with_no_address_is_nobody():
    assert EmailAddress().to_json(CANONICAL) == {}
    assert _contact(emailAddresses=[{"name": ""}]) == _contact()


def test_a_birthday_is_its_date():
    assert _contact(birthday="1953-05-01T00:00:00Z") == _contact(birthday="1953-05-01T11:59:00+00:00")
    assert _contact(birthday="1953-05-01T11:59:00+00:00") != _contact(birthday="1953-05-02T11:59:00+00:00")


def test_a_label_set_has_no_order_and_a_list_that_keeps_it_does():
    assert _contact(categories=["b", "a"]) == _contact(categories=["a", "b"])
    assert _contact(businessPhones=["1", "2"]) != _contact(businessPhones=["2", "1"])


def test_unset_empty_and_partial_addresses_say_nothing():
    assert _contact(homeAddress={}, businessAddress={"city": "Kyiv", "street": None}) == _contact(
        businessAddress={"city": "Kyiv"}
    )


def test_the_wall_clock_has_no_fraction_width():
    sent = _event(start={"dateTime": "2026-03-02T09:00:00.000000", "timeZone": "UTC"})
    read_back = _event(start={"dateTime": "2026-03-02T09:00:00.0000000", "timeZone": "UTC"})
    assert sent == read_back
    assert sent != _event(start={"dateTime": "2026-03-02T09:30:00.0000000", "timeZone": "UTC"})


def test_a_body_is_its_text_not_its_markup():
    plain = _event(body={"contentType": "text", "content": "Agenda"})
    wrapped = _event(body={"contentType": "html", "content": "<html><head><style>p{}</style></head><body>Agenda</body>"})
    assert plain == wrapped


def test_an_attendee_with_no_type_is_a_required_one_and_its_answer_is_not_the_senders():
    asked = _event(attendees=[{"emailAddress": {"address": "a@x.com"}}])
    answered = _event(
        attendees=[{"emailAddress": {"address": "A@x.com"}, "type": "required", "status": {"response": "accepted"}}]
    )
    assert asked == answered
    optional = _event(attendees=[{"emailAddress": {"address": "a@x.com"}, "type": "optional"}])
    assert asked != optional


def test_an_attendee_with_no_address_is_nobody_whatever_its_default():
    assert _event(attendees=[{"type": "optional"}]) == _event()
    assert Attendee().to_json(CANONICAL) == {}


def test_a_location_is_its_name():
    named = _event(location={"displayName": "Room 1"})
    resolved = _event(location={"displayName": "Room 1", "locationType": "default", "uniqueId": "x"})
    assert named == resolved


def test_attendees_are_a_set():
    a, b = {"emailAddress": {"address": "a@x.com"}}, {"emailAddress": {"address": "b@x.com"}}
    assert _event(attendees=[a, b]) == _event(attendees=[b, a])


def test_the_service_owned_columns_never_take_part():
    assert _contact(id="c1", createdDateTime="2020-01-02T03:04:05Z") == _contact()


def test_another_profile_is_unchanged_by_the_declarations():
    contact = Contact(GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})).hydrate(
        {"displayName": "A", "emailAddresses": [{"address": "B@x.com"}], "categories": ["b", "a"]}, V4JsonFormat()
    )
    assert contact.to_json(V4JsonFormat("none")) == {
        "displayName": "A",
        "emailAddresses": [{"address": "B@x.com"}],
        "categories": ["b", "a"],
    }


def test_a_format_nobody_defined_is_refused_when_the_field_is_declared():
    with pytest.raises(ValueError, match="unknown comparison format"):
        Compare(format="roman")


def test_the_location_type_declares_what_the_service_resolves():
    assert Location(displayName="Room 1", uniqueId="x").to_json(CANONICAL) == {"displayName": "Room 1"}


# -- hydrate: the counterpart of to_json -------------------------------------

_ROUND_TRIPS = [
    (
        Contact,
        {
            "displayName": "A",
            "birthday": "1953-05-01T11:59:00+00:00",
            "emailAddresses": [{"address": "b@x.com", "name": "B"}, {"address": "c@x.com"}],
            "businessAddress": {"city": "Kyiv"},
            "categories": ["b", "a"],
        },
    ),
    (
        Event,
        {
            "subject": "Review",
            "start": {"dateTime": "2026-03-02T09:00:00.0000000", "timeZone": "UTC"},
            "attendees": [{"emailAddress": {"address": "a@x.com"}, "type": "optional"}],
            "location": {"displayName": "Room 1"},
            "categories": ["x"],
        },
    ),
]


@pytest.mark.parametrize("model, payload", _ROUND_TRIPS, ids=lambda value: getattr(value, "__name__", "payload"))
def test_an_object_round_trips_through_hydrate(model, payload):
    context = GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})
    held = model(context).hydrate(payload).to_json()
    assert held == model(context).hydrate(held).to_json()
    for profile in (V4JsonFormat("none"), CANONICAL):
        spelled = model(context).hydrate(payload).to_json(profile)
        assert model(context).hydrate(spelled, profile).to_json(profile) == spelled


def test_a_value_has_a_reader_too():
    held = EmailAddress().hydrate({"address": "B@x.com", "name": "B"})
    assert (held.address, held.name) == ("B@x.com", "B")
    assert held.to_json() == {"address": "B@x.com", "name": "B"}
    assert Attendee().hydrate({"emailAddress": {"address": "a@x.com"}, "type": "optional"}).type == "optional"


# -- scoped profiles and the options that choose them --------------------------


def test_a_scoped_profile_narrows_the_model_it_names_and_not_a_nested_value_sharing_a_wire_name():
    contact = Contact(GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})).hydrate(
        {"displayName": "A", "emailAddresses": [{"address": "a@x.com", "name": "A"}], "categories": ["x"]}
    )
    spelled = contact.to_json(V4JsonFormat("none").scoped(Contact, without=("display_name", "categories")))
    assert spelled == {"emailAddresses": [{"address": "a@x.com", "name": "A"}]}
    assert contact.to_json(CANONICAL.scoped(Contact, only=("categories",))) == {"categories": ["x"]}


def test_a_scoped_profile_refuses_a_name_the_model_does_not_declare():
    with pytest.raises(AttributeError, match="not a declared property"):
        V4JsonFormat("none").scoped(Contact, without=("categorys",))


def test_an_option_declares_what_it_governs():
    from dataclasses import dataclass

    from office365.migration.outlook.restore import restores, withheld

    @dataclass
    class Options:
        restore_attendees: bool = restores("attendees", default=False)
        restore_categories: bool = restores("categories", default=True)
        use_transaction_ids: bool = True

    assert withheld(Options()) == ("attendees",)
    assert withheld(Options(restore_attendees=True, restore_categories=False)) == ("categories",)
