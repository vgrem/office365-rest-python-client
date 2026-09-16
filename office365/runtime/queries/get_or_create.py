"""Shared idempotent get-or-create helpers (the metadata analogue of upsert).

The ``ensure_*`` methods across the library all implement the same idea — return
an existing resource or create it — in one of two ways:

- **create-first** (:func:`create_or_get`): queue the create; if the server
  reports a duplicate, load and return the existing resource.
- **get-first** (:func:`get_or_create`): queue a read; if it 404s, queue the
  create in the read's queue slot (so later queries still run after it).

Both centralize the error classification (via the exception registry types) and
the ``copy_from``/``execute_first`` mechanics, so every ``ensure_*`` behaves the
same and a re-run is a no-op. ``on_conflict="update"`` reconciles an existing
resource's definition (the metadata upsert).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Type, TypeVar

from office365.runtime.exceptions import DuplicatedObjectException, ObjectNotFoundException
from office365.runtime.queries.deferred import DeferredOperationQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.queries.client_query import ClientQuery

T = TypeVar("T", bound="ClientObject")

ON_CONFLICT_MODES = ("skip", "update")


def create_or_get(
    create: Callable[[], T],
    find: Callable[[], T],
    *,
    on_duplicate: Type[Exception] = DuplicatedObjectException,
    on_conflict: str = "skip",
    reconcile: Optional[Callable[[T], None]] = None,
) -> T:
    """Queue a create; on a duplicate, load and return the existing resource.

    Args:
        create: Queues the create and returns the new entity.
        find: Queues the read of the existing entity and returns it.
        on_duplicate: The exception type signalling the resource already exists.
        on_conflict: ``"skip"`` (keep existing) or ``"update"`` (reconcile it).
        reconcile: Applied to the existing entity when ``on_conflict="update"``.
    """
    if on_conflict not in ON_CONFLICT_MODES:
        raise ValueError(f"on_conflict must be one of {ON_CONFLICT_MODES}, got {on_conflict!r}")
    return_type = create()

    def _apply(existing: "ClientObject") -> None:
        return_type.copy_from(existing)
        if on_conflict == "update" and callable(reconcile):
            reconcile(return_type)

    def _on_duplicate(error: Exception) -> None:
        if not isinstance(error, on_duplicate):
            raise error
        find().after_execute(_apply, execute_first=True)

    return_type.on_error(_on_duplicate)
    return return_type


def get_or_create(
    find: Callable[[], T],
    create_query: Callable[[], "ClientQuery"],
    return_type: T,
    *,
    on_missing: Type[Exception] = ObjectNotFoundException,
    on_conflict: str = "skip",
    reconcile: Optional[Callable[[T], None]] = None,
) -> T:
    """Queue a read; on a not-found, queue the create in the read's queue slot.

    The create runs in the placeholder's position, so anything queued after the
    ensure still runs after the resource exists (e.g. item creates after field
    creates).

    Args:
        find: Queues the read of the existing entity and returns it.
        create_query: Builds (does not queue) the create query.
        return_type: The entity to populate (existing or created).
        on_missing: The exception type signalling the resource is absent.
        on_conflict: ``"skip"`` (keep existing) or ``"update"`` (reconcile it).
        reconcile: Applied to the existing entity when ``on_conflict="update"``.
    """
    if on_conflict not in ON_CONFLICT_MODES:
        raise ValueError(f"on_conflict must be one of {ON_CONFLICT_MODES}, got {on_conflict!r}")
    context = return_type.context
    barrier = DeferredOperationQuery(context, return_type=return_type)

    def _on_found(existing: "ClientObject") -> None:
        return_type.copy_from(existing)
        if on_conflict == "update" and callable(reconcile):
            reconcile(return_type)
        barrier.resolve()

    def _on_missing(error: Exception) -> None:
        if not isinstance(error, on_missing):
            raise error
        barrier.defer(create_query())

    find().after_execute(_on_found).on_error(_on_missing)
    context.add_query(barrier)
    return return_type
