"""One serialization contract for the model types.

An object, a value, a result and the two collections share no base class, so the contract is
structural (``office365.runtime.serialization``): what a consumer calls is what each of them has.
"""

from __future__ import annotations

from typing import Optional

from office365.graph_client import GraphClient
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.odata.v4.json_format import V4JsonFormat

_CONTEXT = GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})


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


class _City(ClientValue):
    name: Optional[str] = None


class _Holder(ClientValue):
    title: Optional[str] = None
    city: Optional[_City] = None


def test_a_nested_value_with_nothing_to_send_is_omitted():
    # SharePoint 2019 refused the empty nested object an older serializer sent.
    assert _Holder(title="T", city=_City()).to_json() == {"title": "T"}
    assert _Holder(title="T", city=_City(name="Oslo")).to_json() == {"title": "T", "city": {"name": "Oslo"}}
