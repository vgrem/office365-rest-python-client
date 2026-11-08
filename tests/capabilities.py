"""What a live test needs from the tenant: declared once, resolved one way.

A live test states its precondition next to itself — ``@requires_delegated("Mail.Read")``
— and this module is the only place that turns that statement into an answer. The
answer is a :class:`TenantState`: the facts about the signed-in app and user that the
check reads. It is gathered *selectively*, per requirement, because the facts are not
equally available to every token: an app-only client has no ``/me`` to ask for
licenses, and a delegated client may not be allowed to read its own grants. Asking for
a fact the flow cannot see would turn a skipped test into a failing one.

Because one object both *describes* a requirement and *checks* it, the runtime guard,
the skip message and the preflight report cannot disagree.

Nothing here sends a request unless a fact has to be read from the tenant: a fact the client's
own token already proves is read from the token, which costs nothing.

:class:`Requirement` itself lives in the library, next to the declarations a model
method makes, so a test and a method state the same fact with the same type.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Iterable

from office365.directory.licenses.tenant import Licences
from office365.directory.permissions.guard import (
    _cached_app_permissions,
    _cached_delegated_permissions,
    _cached_directory_roles,
)
from office365.graph_client import GraphClient
from office365.permissions import Requirement, TokenClaims
from office365.runtime.client_request_exception import ClientRequestException


@lru_cache(maxsize=1)
def _cached_licenses(client: GraphClient) -> frozenset[str]:
    """The license names the signed-in user holds, memoised for the life of a run.

    The projection is the library's - :attr:`~office365.directory.licenses.tenant.Licences.names`
    returns SKU part numbers *and* provisioned plan names, which is the vocabulary a declaration
    may name. Only the cache is the harness's, because the harness is what knows when a grant
    makes it stale.
    """
    return Licences.of_user(client).names


def forget_cached_tenant_facts() -> None:
    """Drop the memoised permission and license lookups.

    The lookups are ``lru_cache``d for the life of the process, which is right for a test
    run and wrong for a program that has just changed the answer: after granting a
    permission, the same question must be asked again rather than answered from memory.
    """
    for cached in (_cached_delegated_permissions, _cached_app_permissions, _cached_directory_roles, _cached_licenses):
        cached.cache_clear()


@dataclass(frozen=True)
class TenantState:
    """The tenant facts a requirement reads; empty sets mean "not asked for".

    Structurally satisfies :class:`~office365.permissions.requirement.TenantFacts`,
    so ``Requirement`` can check it without importing the harness.
    """

    delegated: frozenset[str] = frozenset()
    application: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    licenses: frozenset[str] = frozenset()
    #: Why the facts could not be read at all (a refused permission lookup).
    unverifiable: str = ""

    @classmethod
    def of(cls, client: GraphClient, client_id: str, requirement: Requirement) -> TenantState:
        """Read exactly the facts ``requirement`` names, or say why they could not be read.

        The client's own token is read first, because it answers the question a skip decision
        asks - will the wire accept this call - and it answers it for the identity that will send
        the request. The tenant's grants are read when the token cannot speak: no token yet, an
        audience for another API, or the other flow.

        A token is not a cheaper spelling of the same question. It is the union over every API
        the identity was consented for, so a scope granted on Exchange reaches a Graph
        requirement through it, where a Graph grant read answers "not granted here" - correctly,
        for the API it was asked about. And it cannot price a grant, because a scope that was
        never granted appears in no token.

        Roles and SKUs are read last, and failing to read them only spoils the answer when the
        requirement *holds* one: a bypass role is an alternative the names can stand without.
        """
        proven = _proven_by_token(client, requirement)
        delegated: frozenset[str] = proven if proven and requirement.delegated else frozenset()
        application: frozenset[str] = proven if proven and requirement.application else frozenset()
        try:
            if proven is None:
                delegated, application = _read_grants(client, client_id, requirement)
        except AttributeError:  # a SharePoint-only client has no Graph surface to read grants from
            return cls(unverifiable="reading the tenant's grants needs a Microsoft Graph client")
        except ClientRequestException:
            return cls(unverifiable="the permission lookup needs a scope this token does not have")
        roles: frozenset[str] = frozenset()
        licenses: frozenset[str] = frozenset()
        try:
            if requirement.roles or requirement.bypass_roles:
                roles = frozenset(role.display_name for role in _cached_directory_roles(client))
            if requirement.licenses:
                licenses = _cached_licenses(client)
        except (AttributeError, ClientRequestException) as exc:
            # Roles and SKUs are the only facts that can be unprovable without making the whole
            # answer unknown, because only they can be stated as an *alternative*: a bypass role
            # says "or this", and the names decide on their own when the role cannot be read. A
            # role or SKU the requirement *holds* is part of the answer, so failing to read it
            # is unverifiable rather than unmet.
            if requirement.roles or requirement.licenses:
                if isinstance(exc, AttributeError):
                    return cls(unverifiable="reading the tenant's grants needs a Microsoft Graph client")
                return cls(unverifiable="the permission lookup needs a scope this token does not have")
        return cls(delegated=delegated, application=application, roles=roles, licenses=licenses)


def _read_grants(client: GraphClient, client_id: str, requirement: Requirement) -> tuple[frozenset[str], frozenset[str]]:
    """The tenant's grants on the requirement's resource, as (delegated names, app roles)."""
    resource = requirement.resource
    delegated = (
        frozenset(_cached_delegated_permissions(client, client_id, resource)) if requirement.delegated else frozenset()
    )
    application = (
        frozenset(role.value for role in _cached_app_permissions(client, client_id, resource))
        if requirement.application
        else frozenset()
    )
    return delegated, application


def held_token(holder: Any) -> str | None:
    """The access token the object's own request context holds, if it has one yet.

    Both a ``GraphClient`` and a SharePoint ``ClientContext`` answer this: the token is kept by
    the request context, and the SharePoint one is the only credential a SharePoint-only suite
    has - which is why a permission check must not require a Graph client to work.
    """
    pending_request = getattr(holder, "pending_request", None)
    if pending_request is None:
        return None
    context = getattr(pending_request(), "authentication_context", None)
    token: str | None = getattr(context, "access_token", None)
    return token


def _proven_by_token(client: GraphClient, requirement: Requirement) -> frozenset[str] | None:
    """The names the client's own token proves for ``requirement``, ``None`` if it cannot say."""
    claims = TokenClaims.parse(held_token(client))
    return None if claims is None else claims.proves(requirement)


@dataclass
class Needs:
    """Every requirement one suite declares, with the tests that declare it.

    ``calls`` is the requirement's provenance: the model methods the declaring tests derived
    it from, as ``module:qualname``. It is keyed *beside* the requirements rather than stored
    on them, because two tests that need the same grant are one line in a report however many
    methods each of them exercised - the requirement is the fact, the calls are where it came
    from.
    """

    suite: str
    flow: str
    tests: int = 0
    requirements: dict[Requirement, list[str]] = field(default_factory=dict)
    calls: dict[Requirement, list[str]] = field(default_factory=dict)

    def add(self, requirement: Requirement, test_name: str, calls: Iterable[str] = ()) -> None:
        """Record that ``test_name`` declares ``requirement``, via the model methods it names."""
        self.requirements.setdefault(requirement, []).append(test_name)
        known = self.calls.setdefault(requirement, [])
        known.extend(call for call in calls if call not in known)

    def unmet_for(self, states: dict[Requirement, TenantState]) -> list[tuple[Requirement, list[str]]]:
        """The requirements these resolved states do not satisfy, with the tests they block.

        A requirement with no resolved state is *not* reported: "not verified" is
        different from "missing", and confusing the two is how a report stops being read.
        """
        return [
            (requirement, tests)
            for requirement, tests in self.requirements.items()
            if (state := states.get(requirement)) is not None and not requirement.satisfied_by(state)
        ]


def declared_requirement(test_method: object) -> Requirement | None:
    """The requirement a decorated test declares, if any — read, never called.

    The decorators stamp the object they return, so the matrix is introspected from
    the tests themselves rather than from a list kept beside them.
    """
    requirement = getattr(test_method, "__requires__", None)
    return requirement if isinstance(requirement, Requirement) else None


def declared_calls(test_method: object) -> tuple[str, ...]:
    """The model methods a decorated test derived its requirement from, as ``module:qualname``.

    Empty for a test that names its scopes by hand: the requirement did not come from the
    library, so there is no call to point at and none is invented.
    """
    calls = getattr(test_method, "__calls__", ())
    return tuple(calls) if isinstance(calls, tuple) else ()
