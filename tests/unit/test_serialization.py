"""One serialization contract, and the one table that decides its spelling.

An object, a value, a result and the two collections share no base class, so the contract is
structural: what a consumer calls is what each of them has. What a profile then *spells* is
decided in one table, so a level cannot answer two ways about the same request.
"""

from __future__ import annotations

from typing import Optional

import pytest
from office365.graph_client import GraphClient
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.value import values_of
from office365.runtime.odata.dialect import V3_VERBOSE, V4
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.odata.v3.metadata_level import ODataV3MetadataLevel
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.odata.v4.metadata_level import ODataV4MetadataLevel

_CONTEXT = GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})


def test_a_result_serializes_the_value_it_carries():
    result = ClientResult(_CONTEXT, EmailAddress("a@x.com", "A"))
    assert result.to_json() == {"address": "a@x.com", "name": "A"}
    assert ClientResult(_CONTEXT, "text").to_json() == "text"


def test_an_object_a_value_and_a_result_all_fill_in_place():
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
    assert Event(_CONTEXT).hydrate(event.to_json()).to_json() == event.to_json()
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


@pytest.mark.parametrize(
    ("profile", "media_type"),
    [
        (JsonLightFormat(), "application/json;odata=verbose"),
        (JsonLightFormat(ODataV3MetadataLevel.MinimalMetadata), "application/json;odata=minimalmetadata"),
        (JsonLightFormat(ODataV3MetadataLevel.NoMetadata), "application/json;odata=nometadata"),
        (
            V4JsonFormat(),
            "application/json;odata.metadata=minimal;odata.streaming=False;IEEE754Compatible=False",
        ),
        (
            V4JsonFormat(ODataV4MetadataLevel.Full),
            "application/json;odata.metadata=full;odata.streaming=False;IEEE754Compatible=False",
        ),
    ],
)
def test_a_level_names_its_own_media_type(profile, media_type):
    assert profile.media_type == media_type


@pytest.mark.parametrize(
    ("profile", "control_information"),
    [
        (JsonLightFormat(), True),
        (JsonLightFormat(ODataV3MetadataLevel.MinimalMetadata), True),
        (JsonLightFormat(ODataV3MetadataLevel.NoMetadata), False),
        (V4JsonFormat(), True),
        (V4JsonFormat(ODataV4MetadataLevel.NoMetadata), False),
    ],
)
def test_only_the_level_that_omits_control_information_omits_it(profile, control_information):
    assert profile.include_control_information is control_information


@pytest.mark.parametrize("profile", [JsonLightFormat("typo"), V4JsonFormat("typo")], ids=["v3", "v4"])
def test_an_unknown_level_falls_back_to_one_row(profile):
    # Before the table carried control information, a profile could claim the verbose
    # spelling and simultaneously write none of it (a ``JsonLightFormat("typo")``).
    assert profile.dialect is profile._default_dialect
    assert profile.include_control_information == profile.dialect.control_information


def test_the_two_families_marker_keys():
    assert V4.type_marker == "@odata.type"
    assert V3_VERBOSE.type_marker == "__metadata"
    assert V3_VERBOSE.type_wrapped
    assert not V4.type_wrapped


@pytest.mark.parametrize(
    "level",
    [ODataV3MetadataLevel.Verbose, ODataV3MetadataLevel.MinimalMetadata, ODataV3MetadataLevel.NoMetadata],
    ids=lambda level: level.value,
)
def test_a_collection_payload_is_the_collection_the_walk_reads_back(level):
    # ``wrap`` writes the envelope and ``iter_payload`` unwraps it; a row that spelled one
    # thing and read another would not round-trip an echo of our own payload.
    fmt = JsonLightFormat(level)
    cell = dict(fmt.iter_payload(fmt.wrap(ClientValueCollection(str, ["a"]), ["a"])))
    assert cell == {0: "a"}
    assert values_of(cell) == ["a"]
