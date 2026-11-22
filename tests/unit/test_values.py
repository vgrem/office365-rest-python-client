"""One seam, two directions: what the service sends becomes a model value, and what it gets back.

A column's declared type decides both — the parser a cell goes through on the way in, and the
spelling a value takes on the way out — so the parser table, the declaration lookup and the two
dialects are pinned here rather than beside the modules they live in.
"""

from __future__ import annotations

import json
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID

import pytest
from office365.booking.appointment import BookingAppointment
from office365.communications.callrecords.call_record import CallRecord
from office365.communications.callrecords.type import CallType
from office365.communications.calls.call import Call
from office365.communications.calls.route import CallRoute
from office365.communications.onlinemeetings.base import OnlineMeetingBase
from office365.communications.onlinemeetings.collection import ChatInfo
from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from office365.directory.applications.application import Application
from office365.directory.audit.signins.activity import SignInActivity
from office365.directory.groups.group import Group
from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.objects.object import DirectoryObject
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.directory.policies.conditionalaccess.grant_controls import ConditionalAccessGrantControls
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from office365.directory.users.password_profile import PasswordProfile
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.entity import Entity
from office365.intune.devices.device import Device
from office365.migration.offline import offline_context
from office365.onedrive.operations.long_running import LongRunningOperation
from office365.onedrive.operations.longrunningoperationstatus import LongRunningOperationStatus
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.named import converter_for
from office365.runtime.converters.records import iter_records
from office365.runtime.converters.scalars import (
    iso_z,
    normalize_guid,
    parse_date,
    parse_datetime,
    parse_decimal,
    parse_duration,
    parse_int,
    parse_uuid,
    wall_clock,
    wall_clock_text,
)
from office365.runtime.converters.value import declared_type, deserialize_value, serialize_value
from office365.runtime.odata.dialect import V3_VERBOSE, V4
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.odata.v3.metadata_level import ODataV3MetadataLevel
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.odata.v4.metadata_level import ODataV4MetadataLevel
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.duration import Duration
from office365.runtime.types.odata_property import odata
from office365.search.hits.container import SearchHitsContainer
from office365.search.response import SearchResponse
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.search.query.sort.sort import Sort
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from requests import Response
from tests import test_site_url

# --- a scalar the wire sends ---------------------------------------------------------


def test_a_duration_column_reads_and_writes_as_a_duration():
    appointment = BookingAppointment(None)
    appointment.set_property("duration", "PT30M")
    assert appointment.duration == timedelta(minutes=30)
    assert appointment.to_json()["duration"] == "PT30M"
    # An assigned ``timedelta`` is written back as the text the service takes.
    appointment.set_property("duration", timedelta(minutes=45))
    assert appointment.to_json()["duration"] == "PT45M"


def test_a_duration_with_no_timedelta_equivalent_is_kept_as_sent():
    # A month is not thirty days, so guessing would be a wrong answer, and dropping it to
    # None would write null back over a value the service reported.
    assert parse_duration("P1M") == "P1M"
    assert parse_duration("P1Y") == "P1Y"
    assert parse_duration("PT") == "PT"
    assert parse_duration(None) is None


def test_a_duration_round_trips_its_seconds():
    # ``Duration.parse`` used to write only hours and minutes, losing them.
    for duration in (
        timedelta(0),
        timedelta(minutes=30),
        timedelta(hours=1, minutes=30),
        timedelta(seconds=90),
        -timedelta(seconds=90),
        timedelta(days=1, hours=2, microseconds=250000),
    ):
        assert parse_duration(Duration.parse(duration)) == duration


def test_a_stamp_and_a_day_are_parsed_apart():
    # A .NET stamp carries seven fraction digits; the fraction is truncated, not refused.
    assert parse_datetime("2026-10-21T09:05:30.0000000+02:00") == datetime(
        2026, 10, 21, 9, 5, 30, tzinfo=timezone(timedelta(hours=2))
    )
    parsed = parse_datetime("2025-01-15T12:34:56.123456+00:00")
    assert parsed is not None
    assert parsed.microsecond == 123456  # noqa: PLR2004
    # ``Edm.Date`` names a day: two equal days must compare equal, whatever the time.
    assert parse_date("2026-01-06T09:00:00Z") == date(2026, 1, 6)
    assert parse_date(datetime(2026, 1, 6, 9, 0)) == date(2026, 1, 6)
    assert parse_date(None) is None
    assert parse_date("not a date") is None


def test_a_wall_clock_keeps_the_literal_not_the_instant():
    # A Graph ``dateTime`` is read with its ``timeZone``, so an offset is dropped, not converted.
    assert wall_clock("2026-10-21T09:05:30.0000000+02:00") == datetime(2026, 10, 21, 9, 5, 30)
    assert wall_clock("2026-10-21T09:05:30Z") == wall_clock("2026-10-21T09:05:30+02:00")
    assert wall_clock("2026-10-21") is None  # a date names no moment
    assert wall_clock("not a date") is None
    assert DateTimeTimeZone(dateTime="2026-05-04T07:00:00.0000000", timeZone="UTC").as_datetime() == datetime(
        2026, 5, 4, 7, 0
    )
    value = DateTimeTimeZone.parse(datetime(2026, 5, 4, 9, 0))
    assert value.dateTime == "2026-05-04T09:00:00.0000000"
    assert value.timeZone == "UTC"


def test_the_z_form_is_what_a_list_item_takes():
    # ``ValidateUpdateListItem`` with ``datesInUTC`` wants the ``...Z`` form, not an offset;
    # a document item parses in the web's locale and rejects a trailing ``Z``.
    assert iso_z("2021-01-01T00:00:00+00:00") == "2021-01-01T00:00:00Z"
    assert iso_z("2021-01-01T00:00:00.123Z") == "2021-01-01T00:00:00Z"
    assert iso_z("not a date") == "not a date"  # passed through, so the service rejection names it
    assert wall_clock_text(datetime(2021, 1, 1, 8, 0, 0)) == "2021-01-01 08:00:00"


def test_an_id_answers_one_spelling():
    # An id arrives braced from a column's ``SchemaXml``, 32-hex from Graph and as
    # ``urn:uuid:`` from a term store. All of them are the same id to a caller.
    guid = "A1B2C3D4-E5F6-4A7B-8C9D-0E1F2A3B4C5D"
    for spelled in (guid, guid.lower(), "{%s}" % guid, "{%s" % guid, guid.replace("-", ""), "urn:uuid:%s" % guid):
        assert normalize_guid(spelled) == guid.lower()
    assert normalize_guid("not a guid") is None
    assert parse_uuid("{%s}" % guid) == UUID(guid.lower())
    # The all-zero GUID is a real answer, not an absent one: it is "no component".
    zero = "00000000-0000-0000-0000-000000000000"
    assert normalize_guid("{%s}" % zero) == zero


def test_a_decimal_is_exact():
    # A float cannot hold 0.1, so an amount round-tripped through it drifts.
    assert parse_decimal("1234.50") == Decimal("1234.50")
    assert parse_decimal(0.1) == Decimal("0.1")
    assert parse_decimal("n/a") is None
    assert parse_int("42") == 42  # noqa: PLR2004
    assert parse_int("abc") is None


# --- the type a column declares ------------------------------------------------------


def test_a_cell_becomes_the_type_it_declares():
    assert declared_type(User, "accountEnabled") is bool
    assert declared_type(User, "createdDateTime") is datetime
    assert declared_type(UserProfile, "userPrincipalName") is str
    activity = SignInActivity()
    activity.set_property("lastSignInDateTime", "2024-01-01T12:00:00Z")
    assert activity.lastSignInDateTime == datetime(2024, 1, 1, 12, tzinfo=timezone.utc)


def test_a_type_imported_inside_the_getter_still_declares():
    # ``ChatInfo`` can only be imported inside the getter: at module level the edge would
    # close a cycle. ``get_type_hints`` saw a bare ``NameError`` and the declaration was
    # lost, so a chatInfo arrived as the dict the service sent.
    assert declared_type(OnlineMeetingBase, "chatInfo") is ChatInfo
    assert declared_type(ConditionalAccessPolicy, "grantControls") is ConditionalAccessGrantControls
    meeting = OnlineMeeting(None)
    meeting.set_property("chatInfo", {"threadId": "19:abc"})
    assert meeting.chat_info.threadId == "19:abc"


class _Unannotated(ClientObject):
    """A hand-written getter that names its type only in the default it returns."""

    @property
    def call_routes(self):
        return self.properties.get("callRoutes", ClientValueCollection(CallRoute))


def test_a_default_is_not_a_declaration():
    # A default passed to ``properties.get`` is a fallback value, not a declaration.
    assert declared_type(_Unannotated, "callRoutes") is None


def test_a_type_stated_in_the_signature_declares():
    # ``Call.call_routes`` named ``CallRoute`` only in its default, so ``callRoutes`` was
    # an unknown column to ``deserialize_records`` and the routes arrived as plain dicts.
    assert declared_type(Call, "callRoutes") == ClientValueCollection[CallRoute]


def test_a_reserved_word_column_resolves():
    # ``CallRecord.type`` is exposed as ``type_``, which ``to_snake_case`` cannot derive.
    assert declared_type(CallRecord, "type") is CallType
    record = CallRecord(offline_context())
    record.set_property("type", "groupCall")
    assert record.type_ is CallType.groupCall


def test_an_enum_value_the_snapshot_does_not_list_is_kept_as_sent():
    # The engine reports ``completed`` where the enum says ``succeeded``. Coercing an
    # unknown member to ``None`` would write null back over what the service reported.
    operation = LongRunningOperation(None)
    operation.set_property("status", "completed")
    assert operation.properties["status"] == "completed"
    operation.set_property("status", "succeeded")
    assert operation.status is LongRunningOperationStatus.succeeded


@pytest.mark.parametrize(
    ("spec", "cell", "expected"),
    [
        ("Edm.DateTimeOffset", "2026-01-06T09:00:00Z", datetime(2026, 1, 6, 9, tzinfo=timezone.utc)),
        ("Edm.Date", "2026-01-06", date(2026, 1, 6)),
        ("Edm.Decimal", "1.10", Decimal("1.10")),
        ("Edm.Int32", "42", 42),
        (datetime, "2026-01-06T09:00:00", datetime(2026, 1, 6, 9)),
        (bool, "yes", True),
    ],
)
def test_a_wire_name_and_a_python_type_resolve_to_one_callable(spec, cell, expected):
    assert converter_for(spec)(cell) == expected


def test_a_name_the_table_does_not_know_is_refused_rather_than_ignored():
    # A typo must not silently mean "no coercion": the column would arrive untyped.
    with pytest.raises(ValueError) as unknown:
        converter_for("datetim")
    assert "datetime" in str(unknown.value)  # the known names are listed
    with pytest.raises(ValueError) as known:
        converter_for("Edm.TimeOfDay")
    assert "time" in str(known.value)
    with pytest.raises(TypeError):
        converter_for(42)  # neither a name, a type, nor a callable


# --- what a value sends --------------------------------------------------------------


def test_a_nested_value_with_nothing_to_send_is_omitted():
    # SharePoint 2019 refused the empty nested object an older serializer sent.
    class City(ClientValue):
        name: str | None = None

    class Holder(ClientValue):
        title: str | None = None
        city: City | None = None

    assert Holder(title="T", city=City()).to_json() == {"title": "T"}
    assert Holder(title="T", city=City(name="Oslo")).to_json() == {"title": "T", "city": {"name": "Oslo"}}
    assert serialize_value(PasswordProfile(password="x", forceChangePasswordNextSignIn=True)) == {
        "password": "x",
        "forceChangePasswordNextSignIn": True,
    }


def test_an_int_enum_is_a_number_in_v3_and_a_name_in_v4():
    assert serialize_value(FieldType.Text, JsonLightFormat()) == 2  # noqa: PLR2004
    assert serialize_value(FieldType.Text, V4JsonFormat()) == "Text"
    assert serialize_value(FieldType.Text) == "Text"


def test_internal_bookkeeping_never_reaches_the_payload():
    # A response bag carries ``__etag``/``__odata_type``/``__deferred``; a request body must
    # not. The dialect's own control marker is rebuilt after the filter, so it survives.
    user = ClientObjectCollection(offline_context(), User, None).create_typed_object(
        {"__etag": 'W/"1"', "__deferred": {"uri": "x"}, "accountEnabled": True}
    )
    assert user.to_json() == {"accountEnabled": True}
    for json_format in (V4JsonFormat(), JsonLightFormat()):
        serialized = user.to_json(json_format)
        assert serialized["accountEnabled"] is True
        for ingested in ("__etag", "__deferred", "__odata_type"):
            assert ingested not in serialized
    assert user.to_json(JsonLightFormat())["__metadata"] == {"type": "microsoft.graph.User"}

    profile = UserProfile()
    profile.set_property("__etag", 'W/"1"')
    profile.set_property("displayName", "A")
    assert profile.to_json()["displayName"] == "A"
    assert "__etag" not in profile.to_json()


def test_a_response_is_not_a_draft():
    # A column the service owns is marked on ingest, so a payload built from a response
    # does not echo it back.
    class Drafted(Entity):
        @odata(name="subject")
        @property
        def subject(self) -> str | None:
            return self.properties.get("subject", None)

        @odata(name="iCalUId", readonly=True)
        @property
        def i_cal_uid(self) -> str | None:
            return self.properties.get("iCalUId", None)

    target = Drafted(None)
    V4JsonFormat().hydrate(target, {"subject": "Q1"})
    assert target.to_json(V4JsonFormat("none")) == {}
    assert target.to_json() == {"subject": "Q1"}


def test_a_collection_is_a_list_for_v4_and_an_envelope_for_json_light():
    assert ClientValueCollection(str, ["a"]).to_json() == ["a"]
    collection = ClientValueCollection(Sort, [Sort(Property="Modified")])
    typename = "Microsoft.SharePoint.Client.Search.Query.Sort"
    payload = JsonLightFormat().build_payload({"SortList": collection})
    assert payload["SortList"]["results"] == [{"Property": "Modified", "__metadata": {"type": typename}}]
    assert payload["SortList"]["__metadata"] == {"type": f"Collection({typename})"}


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
    from office365.runtime.converters.value import values_of

    assert values_of(cell) == ["a"]


# --- what a payload becomes ----------------------------------------------------------


def test_members_are_cast_to_the_type_the_payload_names():
    ctx = ClientContext(test_site_url)
    payload = {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#directoryObjects",
        "value": [
            {"@odata.type": "#microsoft.graph.user", "id": "u1", "displayName": "Alice"},
            {"@odata.type": "#microsoft.graph.group", "id": "g1"},
            {"@odata.type": "#microsoft.graph.device", "id": "d1"},
            {"@odata.type": "#microsoft.graph.application", "id": "a1"},
            {"@odata.type": "#microsoft.graph.servicePrincipal", "id": "sp1"},
        ],
    }
    col = DirectoryObjectCollection(ctx)
    ODataRequest("", V4JsonFormat()).hydrate(col, payload, V4JsonFormat())

    assert [type(item) for item in col] == [User, Group, Device, Application, ServicePrincipal]
    assert col[0].entity_type_name == "microsoft.graph.User"
    for item in col:
        assert "@odata.type" not in item.properties
        assert "__odata_type" not in item.properties
    # A type nobody generated falls back to the base the collection already holds.
    unknown = DirectoryObjectCollection(ctx)
    ODataRequest("", V4JsonFormat()).hydrate(
        unknown, {"value": [{"@odata.type": "#microsoft.graph.administrativeUnit", "id": "au1"}]}, V4JsonFormat()
    )
    assert isinstance(unknown[0], DirectoryObject)
    assert "__odata_type" not in unknown[0].properties


def test_sharepoint_json_light_metadata_stays_out_of_properties():
    ctx = ClientContext(test_site_url)
    web = ctx.web
    ODataRequest(test_site_url, JsonLightFormat()).hydrate(
        web, {"d": {"__metadata": {"type": "SP.Web"}, "Id": "web-1", "Url": "https://x"}}, JsonLightFormat()
    )
    assert web.entity_type_name == "SP.Web"
    assert "__metadata" not in web.properties


def test_hydrate_is_the_mirror_of_to_json():
    ctx = ClientContext(test_site_url)
    for target in (Event(ctx), EmailAddress(), ClientResult(ctx, EmailAddress())):
        read = target.hydrate({"subject": "S"} if isinstance(target, Event) else {"address": "a@x.com"})
        assert read is target
    event = Event(ctx).hydrate({"subject": "S", "categories": ["b", "a"]})
    assert Event(ctx).hydrate(event.to_json()).to_json() == event.to_json()
    assert isinstance(Event(ctx).to_json(), dict)
    assert ClientResult(ctx, EmailAddress()).hydrate({"address": "a@x.com"}).value.address == "a@x.com"


def test_the_profile_decides_how_a_payload_is_read():
    # JSON Light wraps an entity in ``d``; the same mapping means nothing to V4.
    class Holder(ClientValue):
        subject: str | None = None

    payload = {"d": {"subject": "Q1"}}
    assert Holder().hydrate(payload, JsonLightFormat()).subject == "Q1"
    assert Holder().hydrate(payload, V4JsonFormat()).subject is None


def test_a_query_payload_holds_json_ready_scalars():
    # Regression: a raw ``datetime`` in a service-operation payload used to reach
    # ``json.dumps`` unchanged (``createOrGet`` on online meetings failed).
    class Mode(Enum):
        enabled = "enabled"
        disabled = "disabled"

    ctx = ClientContext(test_site_url)
    start = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    query = ServiceOperationQuery(
        ctx.web,
        "createOrGet",
        None,
        {"startDateTime": start, "mode": Mode.disabled, "nested": {"endDateTime": start}, "absent": None},
    )
    payload = ODataRequest(test_site_url, JsonLightFormat())._build_payload(query)
    json.dumps(payload)  # must not raise
    assert payload["startDateTime"] == start.isoformat()
    assert payload["mode"] == "disabled"
    assert payload["nested"]["endDateTime"] == start.isoformat()
    assert "absent" not in payload


def test_raw_content_is_bytes_whatever_the_content_type():
    # A raw-content query (OneDrive ``/content``) returns bytes even when the server
    # reports ``application/json``; anything not JSON is bytes without the flag.
    ctx = ClientContext(test_site_url)
    request = ODataRequest(test_site_url, JsonLightFormat())
    result = ClientResult(ctx, bytes())
    query = FunctionQuery(ctx.web, "content", return_type=result, return_raw_content=True)
    resp = Response()
    resp.status_code = 200
    resp.headers["Content-Type"] = "application/json"
    resp._content = b'{"name": "test"}'
    request.handle_response(resp, query)
    assert result.value == b'{"name": "test"}'


def test_a_coercion_fills_the_object_it_is_given():
    current = PasswordProfile()
    result = deserialize_value(
        PasswordProfile, {"password": "x", "forceChangePasswordNextSignIn": "True"}, current, True
    )
    assert result is current
    assert current.password == "x"
    assert current.forceChangePasswordNextSignIn is True

    response = SearchResponse()
    response.set_property("hitsContainers", [{"hits": [{"contentSource": "x"}], "total": 1}])
    assert isinstance(response.hitsContainers[0], SearchHitsContainer)
    assert response.hitsContainers[0].hits[0].contentSource == "x"


def test_a_record_keeps_the_native_value():
    col = ClientObjectCollection(offline_context(), User, None)
    col.add_child(
        col.create_typed_object(
            {
                "displayName": "John",
                "accountEnabled": True,
                "createdDateTime": datetime(2025, 1, 15, tzinfo=timezone.utc),
            }
        )
    )
    col.query_options.select = ["displayName", "accountEnabled", "createdDateTime"]
    record = iter_records(col)[0]
    assert record["accountEnabled"] is True  # a bool is not spelled back as text
    assert record["createdDateTime"] == "2025-01-15T00:00:00+00:00"


def test_a_collection_field_keeps_the_item_type_its_default_names():
    design = SiteDesignMetadata()
    design.set_property("SiteScriptIds", ["07702c07-0485-426f-b710-4704241caad9"])
    assert isinstance(design.SiteScriptIds, ClientValueCollection)
    assert all(isinstance(item, uuid.UUID) for item in design.SiteScriptIds)


# --- the dialects --------------------------------------------------------------------


def test_the_two_families_marker_keys():
    assert V4.type_marker == "@odata.type"
    assert V3_VERBOSE.type_marker == "__metadata"
    assert V3_VERBOSE.type_wrapped
    assert not V4.type_wrapped


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
    # spelling and simultaneously write none of it.
    assert profile.dialect is profile._default_dialect
    assert profile.include_control_information == profile.dialect.control_information
