"""A licence is bought, so the answer it gives is "not in this tenant" rather than "denied".

A permission can be granted to anyone who asks for it; a licence is bought, and no grant
creates one. When a tenant lacks the plan behind a capability Graph answers ``403`` all the
same, so the caller spends the afternoon re-consenting scopes that were never the problem.
:class:`LicenceGuard` reads the markers declared with
:func:`~office365.permissions.declaration.requires_license` and asks the tenant's own
``subscribedSkus`` whether the call can be made at all - and, for a marker that names a
:data:`~office365.permissions.declaration.USER` seat, asks ``/me/licenseDetails`` whether the
identity making the call owns one. A bought plan and an assigned seat are two reads because they
are two facts: a tenant can hold the licence and the person calling from a shared account hold
none of it.

Three modes, and the default is the quiet one:

``off``
    Sends nothing and checks nothing. A marker is documentation until someone asks otherwise,
    so importing this library in a script costs the same as before.
``warn``
    Reads the tenant's plans once, and logs a warning (once per missing plan) for a call the
    tenant cannot make - then lets it through, because a warning is an observation.
``enforce``
    Raises :class:`LicenceRequired` before the request is built, so nothing is sent.

The tenant read is cached for an hour and failures are cached too: a guard that re-reads on
every call is a second workload, and one that retries a refused read on every call is a storm.
If the read fails outright - typically ``Organization.Read.All`` was never granted - the answer
is *unknown*, and unknown never blocks: a guard that stops calls because it cannot see is worse
than the 403 it was trying to explain.

    >>> client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    >>> client.licence_guard.mode = "warn"
    >>> client.directory.conditional_access_policies.get_all().execute_query()
    WARNING ... ConditionalAccessPolicy needs one of the licences AAD_PREMIUM; ...

Or the same, without touching the script: ``O365_LICENCE_GUARD=enforce o365 ...``.

The guard is given how to learn both facts, and nothing else, so it holds no client and imports
no model: what a tenant or a person holds is a read, and the caller owns it. A caller with no
second reader - an app-only token has no ``/me`` - gets the tenant answer and one note, never a
refusal it could not justify.

    >>> guard = LicenceGuard(
    ...     read=lambda: client.licences.get_all().execute_query().value,
    ...     read_user=lambda: client.licences.get_user(client.me).execute_query().value,
    ... )
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Sequence

from office365.permissions.declaration import TENANT, USER, licence_of, licenses_of

if TYPE_CHECKING:
    from office365.directory.licenses.tenant import LicencesReport
    from office365.runtime.queries.client_query import ClientQuery

#: Sends nothing and checks nothing. What a caller gets unless they ask for more.
OFF = "off"
#: Reads the plans and logs what a call would need; the call is still sent.
WARN = "warn"
#: Raises :class:`LicenceRequired` before the request is built.
ENFORCE = "enforce"

MODES = (OFF, WARN, ENFORCE)

#: The variable a caller sets to choose a mode without editing the program.
ENVIRONMENT = "O365_LICENCE_GUARD"

#: A bought licence changes when an admin assigns it, not between two calls of a script.
SECONDS_PER_HOUR = 3600

logger = logging.getLogger(__name__)


class LicenceRequired(Exception):
    """A call that names a licence was not sent, because the seat it needs holds none of it.

    Raised before the request is built, so it is not a translation of a 403: nothing reached
    the service and nothing needs retrying. ``plans`` is what the marked type declares - a
    family may name several plans as alternatives, and holding any one of them is enough,
    which is why a refusal names all of them. ``seat`` says which fact was missing: the tenant
    bought none of them, or the person making the call was assigned none.
    """

    def __init__(self, plans: Sequence[str], target: str, seat: str = TENANT) -> None:
        self.plans = tuple(plans)
        self.target = target
        self.seat = seat
        missing = (
            "your assignments carry none of them" if seat == USER else "the tenant's subscriptions carry none of them"
        )
        assigned = " assigned to you" if seat == USER else ""
        super().__init__(
            f"{target} needs one of the licences {', '.join(self.plans)}{assigned}; "
            f"{missing}, so nothing was sent. "
            "Set O365_LICENCE_GUARD=warn (or off) to send it anyway."
        )


class LicenceGuard:
    """The tenant's plans, read once, asked before a marked call is sent.

    Reaching this sends nothing: the read happens when a call is about to be made and the guard
    is on, not when the guard is built. ``read`` is the caller's own way of asking the tenant -
    on a :class:`~office365.graph_client.GraphClient` it is one ``subscribedSkus`` read - so the
    guard holds no client and a test can hand over a literal. ``read_user`` is the same bargain
    for the other question: which plans are assigned to the identity making the call, which
    ``/me/licenseDetails`` answers and this guard cannot.
    """

    def __init__(
        self,
        read: Callable[[], LicencesReport],
        read_user: Optional[Callable[[], LicencesReport]] = None,
        mode: str = OFF,
        ttl: int = SECONDS_PER_HOUR,
    ) -> None:
        """
        Args:
            read: How to learn what the tenant holds; returns a
                :class:`~office365.directory.licenses.tenant.LicencesReport`.
            read_user: How to learn what the caller holds - the assignment reader. ``None``
                when there is none, which is the app-only case: an app acts for users but its
                token names none, so the seat question cannot be answered and is not refused.
            mode: One of :data:`MODES`; defaults to ``off``.
            ttl: How long one read of the tenant's plans is trusted, in seconds.
        """
        self._read = read
        self._read_user = read_user
        self._ttl = ttl
        self._report: Optional[LicencesReport] = None
        self._read_at = 0.0
        self._user_plans: Optional[frozenset[str]] = None
        self._user_read_at = 0.0
        self._warned: set[tuple[str, ...]] = set()
        self.mode = mode

    @property
    def mode(self) -> str:
        """What the guard does when a call names a licence: ``off``, ``warn`` or ``enforce``."""
        return self._mode

    @mode.setter
    def mode(self, value: str) -> None:
        if value not in MODES:
            raise ValueError(
                f"{ENVIRONMENT} must be one of {', '.join(MODES)}, not {value!r}: "
                "'off' sends and checks nothing, 'warn' logs, 'enforce' refuses before the request"
            )
        self._mode = value

    @property
    def report(self) -> Optional[LicencesReport]:
        """What the tenant holds, read at most once per ``ttl``; ``None`` when unreadable."""
        now = time.monotonic()
        if self._read_at and now - self._read_at < self._ttl:
            return self._report
        self._read_at = now
        try:
            self._report = self._read()
        except Exception:  # a guard that fails the call it guards is worse than no guard
            self._report = None
            logger.debug("licence guard: the tenant's subscriptions could not be read, so the answer is unknown")
        return self._report

    @property
    def held(self) -> Optional[frozenset[str]]:
        """The service plans provisioned in this tenant; ``None`` when that is unknown."""
        report = self.report
        return report.plans if report is not None else None

    @property
    def names(self) -> Optional[frozenset[str]]:
        """SKU part numbers and plan names together; ``None`` when the tenant is unreadable."""
        report = self.report
        return report.names if report is not None else None

    @property
    def held_by_user(self) -> Optional[frozenset[str]]:
        """The plans assigned to the caller; ``None`` when no reader, or the read failed.

        A bought plan and an assigned seat are different facts, so they are read and cached
        separately: a tenant can hold ``INTUNE_A`` and the person calling from a kiosk account
        can hold no seat at all. Both failures answer ``None`` - unknown - because a guard that
        refuses a call it could not check is worse than the 403 it was explaining.
        """
        if self._read_user is None:
            return None
        now = time.monotonic()
        if self._user_read_at and now - self._user_read_at < self._ttl:
            return self._user_plans
        self._user_read_at = now
        try:
            self._user_plans = self._read_user().plans
        except Exception:  # same rule as the tenant read: an unreadable answer is not a refusal
            self._user_plans = None
            logger.debug("licence guard: the caller's assigned licences could not be read, so the answer is unknown")
        return self._user_plans

    def check(self, target: Any = None, plans: Optional[Iterable[str]] = None, seat: Optional[str] = None) -> None:
        """Ask whether what ``target`` (or ``plans``) requires is held, and by whom it must be.

        The tenant is asked first even for a :data:`USER` seat: a plan nobody bought cannot be
        assigned to anybody, so the cheaper and more certain fact settles it - and it settles it
        with the sentence that names the real cause.

        Args:
            target: A marked type, or a member whose class states one. Ignored when
                ``plans`` is given.
            plans: The plans the call needs, when the caller does not hold a type that
                declares them - a narrowing read off a permission declaration, for instance.
            seat: ``tenant`` or ``user``. ``None`` - the default - asks the type, so a caller
                that holds a marked type never has to know which question it stands for.

        Raises:
            LicenceRequired: In ``enforce`` mode, when the seat that must hold a plan holds none.
        """
        if self.mode == OFF:
            return
        declared = licence_of(target) if seat is None else None
        required = tuple(plans if plans is not None else licenses_of(target))
        if not required:
            return
        seat = declared.seat if declared is not None else (seat or TENANT)
        name = _name_of(target)
        held = self.held
        if held is None:
            self._warn_once(
                ("unknown", name),
                f"cannot tell whether {name} is licensed: the tenant's subscriptions are "
                "unreadable, so the call was not stopped",
            )
            return
        if held.isdisjoint(required):
            self._refuse(required, name, TENANT, "the tenant's subscriptions carry none of them")
            return
        if seat == USER:
            self._check_seat(required, name)

    def _refuse(self, required: tuple[str, ...], name: str, seat: str, missing: str) -> None:
        """Raise in ``enforce``, warn in ``warn``: the same sentence either way."""
        if self.mode == ENFORCE:
            raise LicenceRequired(required, name, seat)
        assigned = " assigned to you" if seat == USER else ""
        self._warn_once(
            (seat,) + required,
            f"{name} needs one of the licences {', '.join(required)}{assigned}; {missing}, and the call was sent anyway",
        )

    def _check_seat(self, required: tuple[str, ...], name: str) -> None:
        """The second question, asked only when the tenant already holds one of the plans."""
        held = self.held_by_user
        if held is None:
            self._warn_once(("unknown-seat", name), self._unknown_seat(name, required))
            return
        if not held.isdisjoint(required):
            return  # the caller holds one of them: any one carries the capability
        self._refuse(required, name, USER, "your assignments carry none of them")

    def _unknown_seat(self, name: str, required: tuple[str, ...]) -> str:
        """Why a seat check could not be made, in the words of whichever reason applies."""
        if self._read_user is None:
            return (
                f"{name} needs one of the licences {', '.join(required)} assigned to the caller, and "
                "this client cannot read that - there is no user reader, as on an app-only token - "
                "so the call was not stopped"
            )
        return (
            f"cannot tell whether {name} is licensed to you: your assigned licences are "
            "unreadable, so the call was not stopped"
        )

    def check_query(self, query: ClientQuery) -> None:
        """Check the type a query speaks for, before the query becomes a request.

        A declaration that narrows the family states more exactly what this call needs, so it is
        asked first; otherwise the query's own types are asked - what it reads, and what it is
        bound to. A collection answers through the type it says it holds, so listing a licensed
        family is checked the same way as reading one of its members.
        """
        if self.mode == OFF:
            return
        declaration = getattr(query, "permission_requirement", None)
        narrowed = tuple(getattr(declaration, "licenses", ()))
        seat = getattr(declaration, "seat", TENANT) if declaration is not None else TENANT
        if narrowed:
            self.check(query.binding_type, plans=narrowed, seat=seat)
            return
        for candidate in (query.return_type, query.binding_type):
            target = _class_of(candidate)
            licence = licence_of(target) if target is not None else None
            if licence is not None and licence.plans:
                self.check(target, plans=licence.plans, seat=licence.seat)
                return

    def _warn_once(self, key: Sequence[str], message: str) -> None:
        """Log a fact once: the same missing plan every call is noise, not information."""
        stamp = tuple(key)
        if stamp in self._warned:
            return
        self._warned.add(stamp)
        logger.warning("%s", message)


def _name_of(target: Any) -> str:
    """What to call the thing in a sentence: its class name, or "this call"."""
    if target is None:
        return "this call"
    owner = _class_of(target)
    return getattr(owner, "__name__", None) or "this call"


def _class_of(value: Any) -> Optional[type]:
    """The type a query names, unwrapping the two ways a collection states one.

    A class is itself. An instance of a collection answers with the item type it declares -
    ``item_type()`` reads the generic base, and a collection built with its type at runtime
    (``EntityCollection(client, Organization, ...)``) keeps it in ``_item_type``. Anything else
    answers with its own class.
    """
    if value is None:
        return None
    if isinstance(value, type):
        return value
    stated = getattr(type(value), "item_type", None)
    if callable(stated):
        found = stated()
        if isinstance(found, type):
            return found
    held = getattr(value, "_item_type", None)
    return held if isinstance(held, type) else type(value)
