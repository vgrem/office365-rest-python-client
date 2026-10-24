"""The comparable spelling of a model: what two spellings of one value have in common.

``entity.to_json(COMPARABLE)`` is the same walk as any other ``to_json``, with one more
reader of the declarations: each field's :class:`~office365.runtime.types.odata_property.Compare`
says what the service treats as the same value, and this profile applies it. A digest of
the result is a digest of the meaning, so a copy the service rewrote (an address-only
email named after itself, a birthday at a time of day nobody set, a label list in another
order) compares equal to what was sent, and a real difference does not.

Everything here works on the *spelled* JSON, so a nested value and a value inside a
collection need no case of their own: they were refined by the same loop, one level down.
A field that says nothing (unset, empty, zero, false) is left out, because a field the
sender omits and a field the service answers empty are the same statement.

**This is a spelling for comparing, never for sending.** A rule may *synthesize* a value the
sender never wrote -- ``Compare.fallback`` names a sibling, ``Compare.default`` names a
value -- because a digest is of the meaning. A request may not: a create body still sends
an address-only attendee with no name. Anything that leaves the process takes a payload
profile (``V4JsonFormat("none")``), never this one.

It is deliberately **not** a canonical form: a canonical form is one representative per
equivalence class that can be turned back into a member of it, and this one is lossy by
construction -- ``Compare.fallback`` and ``Compare.default`` invent values, empty fields
go, lists are sorted. Two different items are *meant* to share one. Hence
``COMPARABLE`` rather than ``CANONICAL``.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional

from office365.runtime.converters.scalars import wall_clock
from office365.runtime.odata.dialect import V4_NO_METADATA
from office365.runtime.odata.json_format import JsonProfile
from office365.runtime.types.odata_property import Compare, ODataPropertyMeta

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
#: Markup whose text is not content, and comments: dropped before a body is reduced to text.
_MARKUP_BLOCK = re.compile(r"<(head|style|script)\b.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")


def _date(value: str) -> str:
    """The calendar date a date-time falls on, whatever time of day is attached."""
    match = _DATE.match(value)
    return match.group(0) if match else value


def _wall_clock(value: str) -> str:
    """The wall clock to the second: the width of the fraction (and any offset) varies
    between what is sent and what comes back.

    A literal with no time of day names no moment, so it cannot be reduced -- and it is
    left as it stands rather than emptied, because two different literals that this rule
    cannot read are still two different statements.
    """
    moment = wall_clock(value)
    return moment.strftime("%Y-%m-%dT%H:%M:%S") if moment else value


def _text(value: str) -> str:
    """A body reduced to its text: the service wraps what it accepts in its own markup."""
    stripped = _MARKUP_BLOCK.sub("", _COMMENT.sub("", value))
    return _SPACE.sub(" ", html.unescape(_TAG.sub(" ", stripped))).strip()


#: The reductions a ``Compare(format=...)`` may name.
FORMATS: Mapping[str, Callable[[str], str]] = {"date": _date, "wall-clock": _wall_clock, "text": _text}


def _order(item: Any) -> str:
    return json.dumps(item, sort_keys=True, default=str)


class ComparableProfile(JsonProfile):
    """Spells a model in its comparable form; see the module docstring."""

    _default_dialect = V4_NO_METADATA

    def __init__(self) -> None:
        super().__init__("none")

    def includes(self, owner: Any, declared: Optional[ODataPropertyMeta], name: str, changed: bool) -> bool:
        """Every present property that is the sender's to state: not a navigation, and
        not one a ``Compare`` hands to someone else."""
        if declared is None:
            return True
        return not (declared.navigation or (declared.compare is not None and declared.compare.ignore))

    def refine(self, spelled: Dict[str, Any], declarations: Iterable[ODataPropertyMeta]) -> Dict[str, Any]:
        rules = {
            declared.name: declared.compare
            for declared in declarations
            if declared.compare is not None and not declared.compare.ignore
        }
        form: Dict[str, Any] = {}
        for name, value in spelled.items():
            rule = rules.get(name)
            reduced = self._reduce(value, rule)
            if reduced:
                form[name] = reduced
        # Nobody: a value without what identifies it says nothing, and a default must not make it
        # look like something.
        if not form or any(rule.key and not form.get(name) for name, rule in rules.items()):
            return {}
        # A field filled in from a sibling, or from a default, reads what is already settled.
        for name, rule in rules.items():
            if form.get(name):
                continue
            filled = form.get(rule.fallback) if rule.fallback else None
            filled = filled if filled else rule.default
            if filled:
                form[name] = filled
        return form

    @staticmethod
    def _reduce(value: Any, rule: Optional[Compare] = None) -> Any:
        """One spelled value under its field's rule; the items of a list under the same rule."""
        if isinstance(value, str):
            value = value.strip()
            if rule is not None and rule.casefold:
                value = value.casefold()
            return FORMATS[rule.format](value) if rule is not None and rule.format else value
        if isinstance(value, list):
            items: List[Any] = [item for item in (ComparableProfile._reduce(item, rule) for item in value) if item]
            return sorted(items, key=_order) if rule is not None and rule.unordered else items
        return value


#: The comparable form: ``entity.to_json(COMPARABLE)``.
COMPARABLE = ComparableProfile()


def digest(form: Any) -> str:
    """A digest of a comparable form: the meaning, not the spelling, and not the bytes.

    ``sort_keys`` so two forms that differ only in field order agree; ``default=str`` so a
    value the walk left un-reduced (a date, an id, a decimal) hashes by its text instead of
    raising. The hash is a checksum, not a signature: a digest finds its twin only if both
    sides ran this same rule, so a checksum written by another build is re-verified once
    rather than trusted.
    """
    return hashlib.md5(json.dumps(form, sort_keys=True, default=str).encode("utf-8")).hexdigest()
