"""A ``IsFlags`` enum names a set of members, and no member names a set.

``authenticationMethodModes`` and ``applicationDataType`` are generated from CSDL
enums carrying ``IsFlags="true"``: the service sends the chosen members joined by
commas (``"password,voice"``), which no single member spells. The conversion used to
answer ``None`` for those -- and a value stored as ``None`` is written back as null on
the next payload, so a policy read from the service and sent back lost the column.
"""

from __future__ import annotations

from office365.directory.applications.data_type import ApplicationDataType
from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.runtime.converters.scalars import parse_enum
from office365.runtime.converters.value import coerce_value


def test_a_combination_of_members_keeps_the_value_the_service_sent() -> None:
    assert parse_enum(AuthenticationMethodModes, "password,voice") == "password,voice"
    # The spelling is the service's: a space after the comma survives, unchanged.
    assert parse_enum(AuthenticationMethodModes, "password, voice") == "password, voice"


def test_a_single_member_is_still_a_member() -> None:
    assert parse_enum(AuthenticationMethodModes, "password") is AuthenticationMethodModes.password
    assert parse_enum(AuthenticationMethodModes, "1") is AuthenticationMethodModes.password


def test_one_unknown_part_is_not_a_combination() -> None:
    """Resolving every part is what separates a combination from an unknown value."""
    assert parse_enum(AuthenticationMethodModes, "password,nonsense") is None
    assert parse_enum(AuthenticationMethodModes, "") is None
    assert parse_enum(ApplicationDataType, "documents") is ApplicationDataType.documents


def test_a_combination_survives_a_round_trip_through_a_payload() -> None:
    """The stored value must reach a request as the service spelled it."""
    stored = coerce_value(AuthenticationMethodModes, "password,voice", AuthenticationMethodModes.password, False)

    assert stored == "password,voice"
