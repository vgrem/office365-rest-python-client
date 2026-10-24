"""What an import option governs, declared on the option.

``restore_attendees: bool = restores("attendees", default=False)`` says which properties of
the model the option switches, once. Everything that has to honour the option (the create
body, the comparable form a digest is made of, the count of what was left out) asks
:func:`withheld` instead of re-spelling the condition.
"""

from __future__ import annotations

from dataclasses import field, fields
from typing import Any, Tuple

_GOVERNS = "migration.restores"


def restores(*attrs: str, default: bool) -> Any:
    """An option field that restores the model's ``attrs`` when it is true."""
    return field(default=default, metadata={_GOVERNS: attrs})


def withheld(options: Any) -> Tuple[str, ...]:
    """The model attributes the options leave out: what each switched-off option governs."""
    return tuple(
        attr
        for declared in fields(options)
        if not getattr(options, declared.name)
        for attr in declared.metadata.get(_GOVERNS, ())
    )
