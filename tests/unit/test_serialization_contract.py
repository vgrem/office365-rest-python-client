"""One serialization contract for the model types.

An object, a value, a result and the two collections share no base class, so the contract is
structural (``office365.runtime.serialization``): what a consumer calls is what each of them has.
These tests state the part that is not just "the method exists".
"""

from __future__ import annotations

import inspect
from typing import Any

import pytest
from office365.graph_client import GraphClient
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.serialization import Hydratable, JsonSerializable, PropertyReceiver

_CONTEXT = GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})


def _instances() -> list[Any]:
    return [
        Event(_CONTEXT),
        EmailAddress("a@x.com", "A"),
        ClientResult(_CONTEXT, EmailAddress("a@x.com")),
        ClientValueCollection(str, ["a"]),
        ClientObjectCollection(_CONTEXT, Contact),
    ]


@pytest.mark.parametrize("instance", _instances(), ids=lambda value: type(value).__name__)
def test_every_model_type_conforms_to_the_protocols(instance):
    assert isinstance(instance, JsonSerializable)
    assert isinstance(instance, Hydratable)
    assert isinstance(instance, PropertyReceiver)


@pytest.mark.parametrize("model", [ClientObject, ClientValue, ClientResult], ids=lambda value: value.__name__)
def test_set_property_spells_its_first_two_parameters_alike(model):
    parameters = list(inspect.signature(model.set_property).parameters)
    assert parameters[:4] == ["self", "name", "value", "persist_changes"]


def test_a_model_defaults_to_intent_and_a_sink_to_as_received():
    default = lambda model: inspect.signature(model.set_property).parameters["persist_changes"].default  # noqa: E731
    assert default(ClientObject) is True and default(ClientValue) is True
    assert default(ClientResult) is False and default(ClientValueCollection) is False


def test_a_result_serializes_the_value_it_carries():
    result = ClientResult(_CONTEXT, EmailAddress("a@x.com", "A"))
    assert result.to_json() == {"address": "a@x.com", "name": "A"}
    assert ClientResult(_CONTEXT, "text").to_json() == "text"


def test_a_value_and_a_result_fill_in_place_like_an_object():
    profile = V4JsonFormat("none")
    value = EmailAddress().hydrate({"address": "a@x.com"}, profile)
    assert value.address == "a@x.com"
    result = ClientResult(_CONTEXT, EmailAddress()).hydrate({"address": "b@x.com"}, profile)
    assert result.value.address == "b@x.com"
    assert Event(_CONTEXT).hydrate({"subject": "S"}, profile).subject == "S"


def test_to_json_answers_a_dict_for_a_model_and_a_list_for_a_collection():
    assert isinstance(Event(_CONTEXT).to_json(), dict)
    assert isinstance(EmailAddress("a@x.com").to_json(), dict)
    assert ClientValueCollection(str, ["a"]).to_json() == ["a"]


def test_hydrate_chains_and_its_default_profile_reads_what_to_json_wrote():
    event = Event(_CONTEXT).hydrate({"subject": "S", "categories": ["b", "a"]})
    assert event.subject == "S"
    copy = Event(_CONTEXT).hydrate(event.to_json())
    assert copy.to_json() == event.to_json()
    value = EmailAddress().hydrate({"address": "a@x.com"})
    assert EmailAddress().hydrate(value.to_json()).to_json() == value.to_json()
    assert ClientResult(_CONTEXT, EmailAddress()).hydrate({"address": "a@x.com"}).value.address == "a@x.com"
