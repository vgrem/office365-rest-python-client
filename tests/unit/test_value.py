"""Offline tests for the shared value serializer (converters/value)."""

from __future__ import annotations

import unittest
import uuid
from datetime import date, datetime, timezone
from enum import Enum
from typing import cast

from office365.directory.users.password_profile import PasswordProfile
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.value import (
    _add_type_metadata,
    declared_type,
    deserialize_value,
    serialize_value,
)
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.types.collections import StringCollection
from office365.search.hits.container import SearchHitsContainer
from office365.search.response import SearchResponse


class _Level(Enum):
    Standard = "standard"
    Premium = "premium"


def _new_user(properties: dict) -> User:
    col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
    return col.create_typed_object(properties)


class TestSerializeValue(unittest.TestCase):
    def test_enum_to_value(self):
        self.assertEqual(serialize_value(_Level.Standard), "standard")

    def test_datetime_to_iso(self):
        value = datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc)
        self.assertEqual(serialize_value(value), "2025-01-15T12:34:56+00:00")

    def test_date_to_iso(self):
        self.assertEqual(serialize_value(date(2025, 1, 15)), "2025-01-15")

    def test_bytes_decoded(self):
        self.assertEqual(serialize_value(b"hello"), "hello")

    def test_uuid_to_str(self):
        value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        self.assertEqual(serialize_value(value), str(value))

    def test_nested_client_value(self):
        profile = PasswordProfile(password="x", forceChangePasswordNextSignIn=True)
        self.assertEqual(serialize_value(profile), {"password": "x", "forceChangePasswordNextSignIn": True})

    def test_nested_client_object(self):
        user = _new_user({"accountEnabled": True, "userPrincipalName": "a@b.c"})
        self.assertEqual(serialize_value(user), {"accountEnabled": True, "userPrincipalName": "a@b.c"})


class TestClientValueToJson(unittest.TestCase):
    def test_user_profile(self):
        profile = UserProfile()
        profile.set_property("accountEnabled", True)
        profile.set_property("passwordProfile", {"password": "x", "forceChangePasswordNextSignIn": True})
        json = profile.to_json()
        self.assertIs(json["accountEnabled"], True)
        self.assertEqual(json["passwordProfile"], {"password": "x", "forceChangePasswordNextSignIn": True})

    def test_collection_to_json(self):
        self.assertEqual(StringCollection(["a", "b"]).to_json(), ["a", "b"])
        self.assertEqual(ClientValueCollection(_Level, [_Level.Standard]).to_json(), ["standard"])


class TestClientObjectToJson(unittest.TestCase):
    def test_user(self):
        user = _new_user({"accountEnabled": True, "userPrincipalName": "a@b.c"})
        self.assertEqual(user.to_json(), {"accountEnabled": True, "userPrincipalName": "a@b.c"})


class TestAddTypeMetadata(unittest.TestCase):
    def test_json_light(self):
        fmt = JsonLightFormat()
        result: dict = {}
        _add_type_metadata(result, fmt, "Microsoft.Graph.User")
        self.assertEqual(result[fmt.metadata_type], {"type": "Microsoft.Graph.User"})

    def test_plain_odata(self):
        fmt = V4JsonFormat()
        result: dict = {}
        _add_type_metadata(result, fmt, "Microsoft.Graph.User")
        self.assertEqual(result[fmt.metadata_type], "#Microsoft.Graph.User")


class TestDeclaredType(unittest.TestCase):
    def test_entity_getter(self):
        self.assertEqual(declared_type(User, "accountEnabled"), bool)
        self.assertIs(declared_type(User, "createdDateTime"), datetime)

    def test_entity_odata_meta(self):
        self.assertEqual(declared_type(User, "passwordProfile"), PasswordProfile)

    def test_dataclass_field(self):
        self.assertEqual(declared_type(UserProfile, "userPrincipalName"), str)
        self.assertEqual(declared_type(UserProfile, "accountEnabled"), bool)
        self.assertEqual(declared_type(PasswordProfile, "forceChangePasswordNextSignIn"), bool)


class TestCoerceValue(unittest.TestCase):
    def test_scalar_bool(self):
        self.assertIs(deserialize_value(bool, "True", None, True), True)
        self.assertIs(deserialize_value(bool, "False", None, True), False)

    def test_scalar_datetime(self):
        value = deserialize_value(datetime, "2025-01-15T12:34:56+00:00", None, True)
        self.assertIsNotNone(value)
        self.assertEqual(value.timetuple()[:6], (2025, 1, 15, 12, 34, 56))

    def test_nested_client_value(self):
        current = PasswordProfile()
        result = deserialize_value(
            PasswordProfile, {"password": "x", "forceChangePasswordNextSignIn": "True"}, current, True
        )
        self.assertIs(result, current)
        self.assertEqual(current.password, "x")
        self.assertIs(current.forceChangePasswordNextSignIn, True)

    def test_generic_collection(self):
        response = SearchResponse()
        response.set_property("hitsContainers", [{"hits": [{"hitId": "x"}], "total": 1}])
        self.assertIsInstance(response.hitsContainers[0], SearchHitsContainer)
        self.assertEqual(response.hitsContainers[0].hits[0].hitId, "x")

    def test_none_stores_none(self):
        profile = UserProfile()
        profile.set_property("givenName", None)
        self.assertIsNone(profile.givenName)


class TestClientResultCoercion(unittest.TestCase):
    def test_enum_keep_on_fail(self):
        result = ClientResult(cast(ClientRuntimeContext, None), _Level.Standard)
        result.set_property("__value", "nope")
        self.assertIs(result.value, _Level.Standard)

    def test_enum_valid(self):
        result = ClientResult(cast(ClientRuntimeContext, None), _Level.Standard)
        result.set_property("__value", "premium")
        self.assertIs(result.value, _Level.Premium)

    def test_datetime(self):
        result = ClientResult(cast(ClientRuntimeContext, None), datetime(2020, 1, 1))
        result.set_property("__value", "2025-01-15T12:34:56Z")
        self.assertEqual(result.value, datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc))

    def test_datetime_keep_on_fail(self):
        result = ClientResult(cast(ClientRuntimeContext, None), datetime(2020, 1, 1))
        result.set_property("__value", "garbage")
        self.assertEqual(result.value, datetime(2020, 1, 1))

    def test_scalar(self):
        result = ClientResult(cast(ClientRuntimeContext, None), "default")
        result.set_property("__value", "hello")
        self.assertEqual(result.value, "hello")


if __name__ == "__main__":
    unittest.main()
