"""What the serialization boundary needs from a model, stated once.

``ClientObject``, ``ClientValue``, ``ClientResult`` and the two collections share no base
class (an object needs a context to exist, a value does not, a result is built by a query),
so the contract is *structural*: a consumer names the one method it calls and anything that
has it conforms. That is the same arrangement as ``os.PathLike`` or ``typing.SupportsInt``;
nothing inherits from these.

``persist_changes`` has two defaults, on purpose. A **model** (an object or a value)
defaults to ``True``: whoever sets a property on it means to write it. A **sink** (a result
or a collection, filled from a response) defaults to ``False``: what arrives is as received,
not a change. ``JsonProfile.hydrate`` always passes the flag explicitly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Protocol, runtime_checkable

from typing_extensions import Self

if TYPE_CHECKING:
    from office365.runtime.odata.json_format import JsonProfile


@runtime_checkable
class JsonSerializable(Protocol):
    """Writes itself as a JSON-compatible value under a profile.

    ``profile=None`` is the value as it is held (a sidecar); a profile spells it for a
    request or for comparison. A model answers a ``dict``, a collection the list of its
    members (wrapped in the dialect's envelope when a profile asks for one).
    """

    def to_json(self, profile: Optional[JsonProfile] = None) -> Any: ...


@runtime_checkable
class Hydratable(Protocol):
    """Reads itself from a payload, in place, and answers itself so the call chains.

    The mirror of :class:`JsonSerializable`. ``profile=None`` is the spelling ``to_json()``
    writes with no profile, so ``x.hydrate(y.to_json())`` round-trips.
    """

    def hydrate(self, payload: Any, profile: Optional[JsonProfile] = None) -> Self: ...


@runtime_checkable
class PropertyReceiver(Protocol):
    """Takes one named property at a time: what ``JsonProfile.hydrate`` fills.

    The key is a property name, or an index when the receiver is list-shaped.
    """

    def set_property(self, name: Any, value: Any, persist_changes: bool = ..., /) -> Any: ...
