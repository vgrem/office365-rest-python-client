"""A licence is bought, so the answer it gives is "not in this tenant" rather than "denied".

A permission can be granted to anyone who asks for it; a licence is bought, and no grant
creates one. When a tenant lacks the plan behind a capability Graph answers ``403`` all the
same, so the caller spends the afternoon re-consenting scopes that were never the problem.
:class:`LicenceGuard` reads the markers declared with
:func:`~office365.permissions.declaration.requires_license` and asks the tenant's own
``subscribedSkus`` whether the call can be made at all.

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

The guard is given one thing - how to learn what the tenant holds - so it holds no client and
imports no model: what a tenant holds is a read, and the caller owns it.

    >>> guard = LicenceGuard(read=lambda: client.licences.get_all().execute_query().value)
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Sequence

from office365.permissions.declaration import licenses_of

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
    """A call that names a licence was not sent, because no plan in this tenant carries it.

    Raised before the request is built, so it is not a translation of a 403: nothing reached
    the service and nothing needs retrying. ``plans`` is what the marked type declares - a
    family may name several plans as alternatives, and holding any one of them is enough,
    which is why a refusal names all of them.
    """

    def __init__(self, plans: Sequence[str], target: str) -> None:
        self.plans = tuple(plans)
        self.target = target
        super().__init__(
            f"{target} needs one of the licences {', '.join(self.plans)}; this tenant's "
            "subscriptions carry none of them, so nothing was sent. "
            "Set O365_LICENCE_GUARD=warn (or off) to send it anyway."
        )


class LicenceGuard:
    """The tenant's plans, read once, asked before a marked call is sent.

    Reaching this sends nothing: the read happens when a call is about to be made and the guard
    is on, not when the guard is built. ``read`` is the caller's own way of asking the tenant -
    on a :class:`~office365.graph_client.GraphClient` it is one ``subscribedSkus`` read - so the
    guard holds no client and a test can hand over a literal.
    """

    def __init__(
        self,
        read: Callable[[], LicencesReport],
        mode: str = OFF,
        ttl: int = SECONDS_PER_HOUR,
    ) -> None:
        """
        Args:
            read: How to learn what the tenant holds; returns a
                :class:`~office365.directory.licenses.tenant.LicencesReport`.
            mode: One of :data:`MODES`; defaults to ``off``.
            ttl: How long one read of the tenant's plans is trusted, in seconds.
        """
        self._read = read
        self._ttl = ttl
        self._report: Optional[LicencesReport] = None
        self._read_at = 0.0
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

    def check(self, target: Any = None, plans: Optional[Iterable[str]] = None) -> None:
        """Ask whether this tenant holds what ``target`` (or ``plans``) requires.

        Args:
            target: A marked type, or a member whose class states one. Ignored when
                ``plans`` is given.
            plans: The plans the call needs, when the caller does not hold a type that
                declares them - a narrowing read off a permission declaration, for instance.

        Raises:
            LicenceRequired: In ``enforce`` mode, when the tenant holds none of the plans.
        """
        if self.mode == OFF:
            return
        required = tuple(plans if plans is not None else licenses_of(target))
        if not required:
            return
        name = _name_of(target)
        held = self.held
        if held is None:
            self._warn_once(
                ("unknown", name),
                f"cannot tell whether {name} is licensed: the tenant's subscriptions are "
                "unreadable, so the call was not stopped",
            )
            return
        if not held.isdisjoint(required):
            return  # any one of the named plans carries the capability
        if self.mode == ENFORCE:
            raise LicenceRequired(required, name)
        self._warn_once(
            required,
            f"{name} needs one of the licences {', '.join(required)}; the tenant's "
            "subscriptions carry none of them, and the call was sent anyway",
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
        if narrowed:
            self.check(query.binding_type, plans=narrowed)
            return
        for candidate in (query.return_type, query.binding_type):
            target = _class_of(candidate)
            if target is not None and licenses_of(target):
                self.check(target)
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
