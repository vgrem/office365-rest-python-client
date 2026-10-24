"""``Compare`` rules say something their field's type can bear (see ``runtime/compare_check.py``)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pytest
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_value import ClientValue
from office365.runtime.compare_check import compare_problems
from office365.runtime.types.odata_property import Compare, odata


@pytest.mark.parametrize("model", [Event, Contact, Message], ids=lambda model: model.__name__)
def test_every_declared_compare_rule_fits_its_field(model):
    assert compare_problems(model) == []


def _problems(**declared) -> list:
    @dataclass
    class Sample(ClientValue):
        text: Optional[str] = field(default=None, metadata=odata("text", compare=declared.get("text")))
        when: Optional[datetime] = field(default=None, metadata=odata("when", compare=declared.get("when")))
        number: Optional[int] = field(default=None, metadata=odata("number", compare=declared.get("number")))
        label: Optional[str] = field(default=None, metadata=odata("label", compare=declared.get("label")))

    return compare_problems(Sample)


def test_unordered_on_a_scalar_is_reported():
    assert "unordered needs a collection" in _problems(text=Compare(unordered=True))[0]


def test_a_format_on_the_wrong_type_is_reported():
    assert "format 'wall-clock' needs" in _problems(number=Compare(format="wall-clock"))[0]
    assert _problems(when=Compare(format="date")) == []


def test_casefold_on_a_number_is_reported():
    assert "casefold needs text" in _problems(number=Compare(casefold=True))[0]


def test_a_fallback_must_name_a_sibling():
    assert "not a sibling field" in _problems(text=Compare(fallback="nowhere"))[0]
    assert _problems(text=Compare(fallback="label")) == []


def test_ignore_contradicts_the_rules_that_make_a_field_take_part():
    assert "ignore contradicts" in _problems(text=Compare(ignore=True, key=True))[0]
