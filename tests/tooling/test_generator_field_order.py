"""Where a new dataclass field lands: after every field the class already requires.

``SourceEditor`` keeps the field block in wire-name order, but name order is not the
whole rule: ``dataclass`` raises ``TypeError: non-default argument 'Title' follows
default argument 'ChannelNotes'`` for a defaulted field that precedes a required one.
The block is therefore two runs -- required, then defaulted -- and each is spliced by
name. Every case below ends in ``exec``, so the assertion is the one Python makes:
:func:`dataclasses.fields` and ``__init__`` are built or the test fails.
"""

from __future__ import annotations

import ast
import dataclasses
from typing import Optional, Type

from generator.edit.source_editor import SourceEditor

_SOURCE = """\
class Widget(ClientValue):
    Title: str
    Url: str
    Owner: Optional[str] = None
    Zeta: int = 1

    @property
    def entity_type_name(self):
        return "SP.Widget"
"""


class _Notes:
    """Stand-in for a complex value: a zero-argument factory is all a default needs."""


def _base() -> Type[object]:
    """A base whose hook runs ``dataclass`` on the subclass, as ``ClientValue`` does."""

    class _ClientValue:
        def __init_subclass__(cls, **kwargs: object) -> None:
            super().__init_subclass__(**kwargs)
            dataclasses.dataclass(cls)

    return _ClientValue


def _fields_after(field_code: str) -> list[str]:
    """Splice ``field_code`` into ``_SOURCE`` and return the dataclass's field order."""
    member = ast.parse(field_code.strip()).body[0]
    spliced = SourceEditor(_SOURCE, "Widget").splice([member], [])
    namespace: dict[str, object] = {
        "ClientValue": _base(),
        "Optional": Optional,
        "field": dataclasses.field,
        "Notes": _Notes,
    }
    exec(compile(spliced, "<spliced>", "exec"), namespace)  # noqa: S102 - the artefact under test
    return [field.name for field in dataclasses.fields(namespace["Widget"])]


def test_a_defaulted_field_goes_after_the_required_ones_not_before() -> None:
    """``ChannelNotes`` sorts before ``Title``; ``dataclass`` refuses to let it go first."""
    assert _fields_after("ChannelNotes: Notes = field(default_factory=Notes)") == [
        "Title",
        "Url",
        "ChannelNotes",
        "Owner",
        "Zeta",
    ]


def test_a_defaulted_field_keeps_name_order_within_its_own_run() -> None:
    """Name order still decides where in the defaulted run a field lands."""
    assert _fields_after("Willow: Optional[str] = None") == ["Title", "Url", "Owner", "Willow", "Zeta"]


def test_a_defaulted_field_that_sorts_last_stays_in_the_block() -> None:
    """Not appended after ``entity_type_name``, which would split the block in two."""
    assert _fields_after("Zulu: Optional[str] = None") == ["Title", "Url", "Owner", "Zeta", "Zulu"]


def test_a_required_field_opens_the_block() -> None:
    """A field without a default cannot follow the defaulted run either."""
    assert _fields_after("Caption: str") == ["Caption", "Title", "Url", "Owner", "Zeta"]


def test_the_target_class_is_the_one_the_file_names() -> None:
    """A module may declare helpers; only the class being updated receives the member."""
    source = """\
class Helper:
    pass


class Widget(ClientValue):
    Title: str
"""
    member = ast.parse("Owner: Optional[str] = None").body[0]
    spliced = SourceEditor(source, "Widget").splice([member], [])
    tree = ast.parse(spliced)
    declared = {
        node.name: [stmt.target.id for stmt in node.body if isinstance(stmt, ast.AnnAssign)]
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    assert not declared["Helper"]
    assert declared["Widget"] == ["Title", "Owner"]
