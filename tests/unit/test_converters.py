"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import unittest
import uuid
from datetime import datetime, timedelta, timezone
from typing import cast

from office365.booking.appointment import BookingAppointment
from office365.communications.callrecords.call_record import CallRecord
from office365.communications.callrecords.type import CallType
from office365.communications.calls.call import Call
from office365.communications.calls.route import CallRoute
from office365.communications.onlinemeetings.base import OnlineMeetingBase
from office365.communications.onlinemeetings.collection import ChatInfo
from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.directory.policies.conditionalaccess.grant_controls import ConditionalAccessGrantControls
from office365.directory.users.password_profile import PasswordProfile
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.records import iter_records
from office365.runtime.converters.scalars import (
    iso_z,
    normalize_guid,
    parse_datetime,
    parse_duration,
    parse_int,
    wall_clock,
    wall_clock_text,
)
from office365.runtime.converters.value import _declared_cache, coerce_value, declared_type, serialize_value
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.types.duration import Duration
from office365.search.hits.container import SearchHitsContainer
from office365.search.response import SearchResponse
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata


class _Unannotated(ClientObject):
    """A hand-written getter that names its type only in the default it returns."""

    @property
    def call_routes(self):
        return self.properties.get("callRoutes", ClientValueCollection(CallRoute))


class TestCyclicDeclaredType(unittest.TestCase):
    """A type too cyclic for a module-level import is still the getter's declared type."""

    def setUp(self):
        _declared_cache.clear()

    def test_a_type_the_getter_imports_for_itself_declares(self):
        # ``ChatInfo``/``ConditionalAccessGrantControls`` can only be imported inside the
        # getter: at module level the edge would close a cycle. ``get_type_hints`` saw a
        # bare ``NameError`` and the declaration was lost, so a chatInfo arrived as the
        # dict the service sent.
        self.assertIs(declared_type(OnlineMeetingBase, "chatInfo"), ChatInfo)
        self.assertIs(declared_type(ConditionalAccessPolicy, "grantControls"), ConditionalAccessGrantControls)

    def test_the_value_is_built_from_the_declaration(self):
        meeting = OnlineMeeting(None)
        meeting.set_property("chatInfo", {"threadId": "19:abc"})
        self.assertIsInstance(meeting.chat_info, ChatInfo)
        self.assertEqual(meeting.chat_info.threadId, "19:abc")

    def test_a_getter_that_annotates_nothing_still_declares_nothing(self):
        # An annotation is what states a type. A default passed to ``properties.get``
        # is a fallback value, not a declaration, so a getter that states nothing is
        # read as ``None`` -- which is why the unannotated ones were backfilled rather
        # than taught to the resolver.
        self.assertIsNone(declared_type(_Unannotated, "callRoutes"))

    def test_a_getter_that_states_its_type_in_the_signature_declares_it(self):
        # ``Call.call_routes`` used to name ``CallRoute`` only in the default it passed
        # to ``properties.get``, so ``callRoutes`` was an unknown column to
        # ``coerce_records`` and the service's routes arrived as plain dicts.
        self.assertEqual(declared_type(Call, "callRoutes"), ClientValueCollection[CallRoute])


class TestDuration(unittest.TestCase):
    """``Edm.Duration`` is text on the wire and a ``timedelta`` in the model."""

    def test_the_forms_the_service_sends(self):
        self.assertEqual(parse_duration("PT30M"), timedelta(minutes=30))
        self.assertEqual(parse_duration("PT1H30M"), timedelta(hours=1, minutes=30))
        self.assertEqual(parse_duration("P1DT2H"), timedelta(days=1, hours=2))
        self.assertEqual(parse_duration("PT0S"), timedelta(0))
        self.assertEqual(parse_duration("-PT1M30S"), -timedelta(seconds=90))
        self.assertEqual(parse_duration(timedelta(minutes=5)), timedelta(minutes=5))

    def test_a_form_with_no_timedelta_equivalent_is_kept_as_sent(self):
        # A month is not thirty days, so guessing would be a wrong answer, and dropping
        # it to None would write null back over a value the service reported.
        self.assertEqual(parse_duration("P1M"), "P1M")
        self.assertEqual(parse_duration("P1Y"), "P1Y")
        self.assertEqual(parse_duration("PT"), "PT")
        self.assertEqual(parse_duration(None), None)

    def test_a_round_trip_keeps_the_seconds(self):
        """``Duration.parse`` used to write only hours and minutes, losing them."""
        for duration in (
            timedelta(0),
            timedelta(minutes=30),
            timedelta(hours=1, minutes=30),
            timedelta(seconds=90),
            -timedelta(seconds=90),
            timedelta(days=1, hours=2, microseconds=250000),
        ):
            with self.subTest(duration=duration):
                self.assertEqual(parse_duration(Duration.parse(duration)), duration)

    def test_a_duration_column_reads_and_writes_as_a_duration(self):
        appointment = BookingAppointment(None)
        appointment.set_property("duration", "PT30M")
        self.assertEqual(appointment.duration, timedelta(minutes=30))
        self.assertEqual(appointment.to_json()["duration"], "PT30M")
        # An assigned ``timedelta`` is written back as the text the service takes.
        appointment.set_property("duration", timedelta(minutes=45))
        self.assertEqual(appointment.to_json()["duration"], "PT45M")


class TestScalarConverters(unittest.TestCase):
    def test_parse_datetime_offset_with_microseconds(self):
        value = "2025-01-15T12:34:56.123456+00:00"
        parsed = parse_datetime(value)
        assert parsed is not None
        self.assertEqual(parsed.microsecond, 123456)

    def test_parse_datetime_with_seven_fraction_digits(self):
        """A .NET stamp carries seven digits; the fraction is truncated, not refused."""
        parsed = parse_datetime("2026-10-21T09:05:30.0000000+02:00")
        assert parsed is not None
        self.assertEqual(parsed, datetime(2026, 10, 21, 9, 5, 30, tzinfo=timezone(timedelta(hours=2))))
        self.assertEqual(parse_datetime("2026-10-21T09:05:30.1234567Z").microsecond, 123456)

    def test_wall_clock_keeps_the_literal_not_the_instant(self):
        """A Graph ``dateTime`` is read with its ``timeZone``, so an offset is dropped, not converted."""
        self.assertEqual(wall_clock("2026-10-21T09:05:30.0000000+02:00"), datetime(2026, 10, 21, 9, 5, 30))
        self.assertEqual(wall_clock("2026-10-21T09:05:30Z"), wall_clock("2026-10-21T09:05:30+02:00"))
        # A date names no moment: a recurrence endDate is not midnight.
        self.assertIsNone(wall_clock("2026-10-21"))
        self.assertIsNone(wall_clock(None))
        self.assertIsNone(wall_clock("not a date"))

    def test_iso_z_is_the_utc_spelling_a_list_item_takes(self):
        """``ValidateUpdateListItem`` with ``datesInUTC`` wants the ``...Z`` form, not an offset."""
        self.assertEqual(iso_z("2021-01-01T00:00:00+00:00"), "2021-01-01T00:00:00Z")
        self.assertEqual(iso_z("2021-01-01T00:00:00"), "2021-01-01T00:00:00Z")
        self.assertEqual(iso_z("2021-01-01T00:00:00.123Z"), "2021-01-01T00:00:00Z")
        self.assertIsNone(iso_z(None))
        self.assertIsNone(iso_z(""))
        # An unreadable literal is passed through, so the service rejection names it.
        self.assertEqual(iso_z("not a date"), "not a date")

    def test_wall_clock_text_is_the_local_spelling_a_document_item_takes(self):
        """A document item parses in the web's locale and rejects a trailing ``Z``."""
        self.assertEqual(wall_clock_text(datetime(2021, 1, 1, 8, 0, 0)), "2021-01-01 08:00:00")
        self.assertEqual(wall_clock_text("2021-01-01T08:00:00"), "2021-01-01T08:00:00")
        self.assertIsNone(wall_clock_text(None))

    def test_normalize_guid_answers_one_spelling_for_every_form(self):
        """An id arrives braced from a column's ``SchemaXml`` and bare from a payload."""
        guid = "A1B2C3D4-E5F6-4A7B-8C9D-0E1F2A3B4C5D"
        for spelled in (guid, guid.lower(), "{%s}" % guid, "  %s  " % guid):
            self.assertEqual(normalize_guid(spelled), guid.lower())
        self.assertIsNone(normalize_guid(None))
        self.assertIsNone(normalize_guid(""))
        self.assertIsNone(normalize_guid("not a guid"))
        # A stray brace is forgiven rather than reflected: what a caller keys on is the
        # id, and the old spelling returned the brace it had failed to strip, so the
        # same list arrived under two keys.
        self.assertEqual(normalize_guid("{%s" % guid), guid.lower())
        # The two forms a hand-rolled pattern refused: the same id arrives 32-hex from a
        # Graph payload and as ``urn:uuid:`` from a term store.
        self.assertEqual(normalize_guid(guid.replace("-", "")), guid.lower())
        self.assertEqual(normalize_guid("urn:uuid:%s" % guid), guid.lower())
        # The all-zero GUID is a real answer, not an absent one: SharePoint writes it
        # for "no component", which a caller must be able to tell from "not a GUID".
        zero = "00000000-0000-0000-0000-000000000000"
        self.assertEqual(normalize_guid("{%s}" % zero), zero)


def _new_user(properties: dict) -> User:
    col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
    return col.create_typed_object(properties)


class TestSerializeValue(unittest.TestCase):
    def test_nested_client_value(self):
        profile = PasswordProfile(password="x", forceChangePasswordNextSignIn=True)
        self.assertEqual(serialize_value(profile), {"password": "x", "forceChangePasswordNextSignIn": True})

    def test_int_enum_serialization_is_format_dependent(self):
        # SharePoint (OData V3) enums are Edm.Int32 -> numeric value.
        from office365.sharepoint.fields.type import FieldType

        self.assertEqual(serialize_value(FieldType.Text, JsonLightFormat()), 2)
        # OData V4 / Graph enums keep the member name.
        self.assertEqual(serialize_value(FieldType.Text, V4JsonFormat()), "Text")
        self.assertEqual(serialize_value(FieldType.Text), "Text")


class TestClientValueToJson(unittest.TestCase):
    def test_user_profile(self):
        profile = UserProfile()
        profile.set_property("accountEnabled", True)
        profile.set_property("passwordProfile", {"password": "x", "forceChangePasswordNextSignIn": True})
        json = profile.to_json()
        assert isinstance(json, dict)
        self.assertIs(json["accountEnabled"], True)
        self.assertEqual(json["passwordProfile"], {"password": "x", "forceChangePasswordNextSignIn": True})

    def test_internal_bookkeeping_is_not_a_field(self):
        # ``__etag`` is ingested from a response so ``If-Match`` can be built; it
        # describes the response, so it must not appear in a serialized value.
        profile = UserProfile()
        profile.set_property("__etag", 'W/"1"')
        profile.set_property("displayName", "A")
        serialized = profile.to_json()
        self.assertNotIn("__etag", serialized)
        self.assertEqual(serialized["displayName"], "A")


class TestClientObjectToJson(unittest.TestCase):
    def test_internal_bookkeeping_never_reaches_the_payload(self):
        # A response bag carries ``__etag``/``__odata_type``/``__deferred``; a request
        # body must not, in either dialect.
        user = _new_user({"__etag": 'W/"1"', "__deferred": {"uri": "x"}, "accountEnabled": True})
        self.assertEqual(user.to_json(), {"accountEnabled": True})
        for json_format in (V4JsonFormat(), JsonLightFormat()):
            serialized = user.to_json(json_format)
            self.assertEqual(serialized["accountEnabled"], True)
            for ingested in ("__etag", "__deferred", "__odata_type"):
                self.assertNotIn(ingested, serialized)
        # The dialect's own control marker is rebuilt after the filter, so it survives
        # while the response's is gone.
        self.assertEqual(user.to_json(JsonLightFormat())["__metadata"], {"type": "microsoft.graph.User"})


class TestDateTimeTimeZone(unittest.TestCase):
    def test_a_datetime_becomes_the_canonical_wire_form(self):
        # Graph reads `dateTime` as a wall clock and takes the zone from `timeZone`,
        # so the fraction is Graph's seven digits and no offset is appended.
        value = DateTimeTimeZone.parse(datetime(2026, 5, 4, 9, 0))
        self.assertEqual(value.dateTime, "2026-05-04T09:00:00.0000000")
        self.assertEqual(value.timeZone, "UTC")
        self.assertEqual(value.to_json(), {"dateTime": "2026-05-04T09:00:00.0000000", "timeZone": "UTC"})

    def test_as_datetime_reads_the_wall_clock(self):
        value = DateTimeTimeZone(dateTime="2026-05-04T07:00:00.0000000", timeZone="UTC")
        self.assertEqual(value.as_datetime(), datetime(2026, 5, 4, 7, 0))
        self.assertIsNone(DateTimeTimeZone().as_datetime())
        self.assertIsNone(DateTimeTimeZone(dateTime="not a date").as_datetime())


class TestDeclaredType(unittest.TestCase):
    def test_entity_getter(self):
        self.assertEqual(declared_type(User, "accountEnabled"), bool)
        self.assertIs(declared_type(User, "createdDateTime"), datetime)

    def test_sign_in_activity_parses_datetime(self):
        from office365.directory.audit.signins.activity import SignInActivity

        activity = SignInActivity()
        activity.set_property("lastSignInDateTime", "2024-01-01T12:00:00Z")
        self.assertIsInstance(activity.lastSignInDateTime, datetime)
        self.assertEqual(activity.lastSignInDateTime, datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc))

    def test_dataclass_field(self):
        self.assertEqual(declared_type(UserProfile, "userPrincipalName"), str)
        self.assertEqual(declared_type(UserProfile, "accountEnabled"), bool)
        self.assertEqual(declared_type(PasswordProfile, "forceChangePasswordNextSignIn"), bool)

    def test_entity_reserved_word_getter(self):
        # ``CallRecord.type`` is exposed as ``type_`` (a reserved word), which
        # ``to_snake_case`` cannot derive — the trailing-underscore fallback must.
        self.assertIs(declared_type(CallRecord, "type"), CallType)
        record = CallRecord(cast(ClientRuntimeContext, None))
        record.set_property("type", "groupCall")
        self.assertIs(record.type_, CallType.groupCall)


class TestCoerceValue(unittest.TestCase):
    def test_nested_client_value(self):
        current = PasswordProfile()
        result = coerce_value(PasswordProfile, {"password": "x", "forceChangePasswordNextSignIn": "True"}, current, True)
        self.assertIs(result, current)
        self.assertEqual(current.password, "x")
        self.assertIs(current.forceChangePasswordNextSignIn, True)

    def test_generic_collection(self):
        response = SearchResponse()
        response.set_property("hitsContainers", [{"hits": [{"contentSource": "x"}], "total": 1}])
        self.assertIsInstance(response.hitsContainers[0], SearchHitsContainer)
        self.assertEqual(response.hitsContainers[0].hits[0].contentSource, "x")


class TestClientResultCoercion(unittest.TestCase):
    def test_parse_int(self):
        self.assertEqual(parse_int("42"), 42)
        self.assertEqual(parse_int(7), 7)
        self.assertIsNone(parse_int(None))
        self.assertIsNone(parse_int("abc"))


def _collection(properties: list[dict]) -> ClientObjectCollection:
    col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


class TestIterRecords(unittest.TestCase):
    def test_native_values_kept(self):
        col = _collection(
            [
                {
                    "displayName": "John",
                    "accountEnabled": True,
                    "createdDateTime": datetime(2025, 1, 15, tzinfo=timezone.utc),
                }
            ]
        )
        col.query_options.select = ["displayName", "accountEnabled", "createdDateTime"]
        record = iter_records(col)[0]
        self.assertIs(record["accountEnabled"], True)
        self.assertEqual(record["createdDateTime"], "2025-01-15T00:00:00+00:00")


class TestSiteDesignMetadataDefaults(unittest.TestCase):
    """ClientValueCollection-typed fields keep their item type from defaults."""

    def test_parses_non_empty_site_script_ids(self):
        design = SiteDesignMetadata()
        design.set_property(
            "SiteScriptIds",
            ["07702c07-0485-426f-b710-4704241caad9", "6250ceba-8724-4fb4-8c52-5a89183b9587"],
        )

        assert isinstance(design.SiteScriptIds, ClientValueCollection)
        assert len(design.SiteScriptIds) == 2  # noqa: PLR2004
        assert all(isinstance(item, uuid.UUID) for item in design.SiteScriptIds)
