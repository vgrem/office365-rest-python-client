"""A licence is bought, so a refusal cannot be a translation of a ``403``.

What is asserted here is the shape of the decision, not the words: the guard sends nothing
until it is asked to, reads the tenant once, refuses *before* a token is asked for, treats an
unreadable tenant as unknown rather than absent, and answers a family from any one of the plans
it names. The catalogue of which plan carries which feature is Microsoft's data, so no test
restates it.
"""

from __future__ import annotations

import unittest.mock
from typing import TYPE_CHECKING, Any, cast

import pytest
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.licensing import ENFORCE, OFF, WARN, LicenceGuard, LicenceRequired
from office365.permissions.declaration import requires_license
from office365.runtime.queries.client_query import ClientQuery

if TYPE_CHECKING:
    from office365.directory.licenses.tenant import LicencesReport

#: The number this file exists to keep at one; the ttl case is the only one that asks twice.
ONE_READ = 1
TWO_READS = 2


class Plans:
    """What a tenant holds, in the two vocabularies ``subscribedSkus`` answers in."""

    def __init__(self, *plans: str) -> None:
        self.plans = frozenset(plans)
        self.names = self.plans


def nothing() -> LicencesReport:
    """A tenant that holds no plan at all, readable the way a client's licences are."""
    return cast("LicencesReport", Plans())


def guard_of(*plans: str, mode: str = ENFORCE, ttl: int = 3600) -> tuple[LicenceGuard, unittest.mock.Mock]:
    """A guard whose tenant is known, and the counter that shows how often it was asked."""
    read = unittest.mock.Mock(return_value=Plans(*plans))
    return LicenceGuard(read=read, mode=mode, ttl=ttl), read


@requires_license("AAD_PREMIUM", "AAD_PREMIUM_P2")
class TwoPlans:
    """A family a tenant may have bought either way."""


def test_off_sends_nothing_and_reads_nothing() -> None:
    read = unittest.mock.Mock(side_effect=AssertionError("off must not read the tenant"))
    guard = LicenceGuard(read=read)
    assert guard.mode == OFF
    guard.check_query(_query(User))
    read.assert_not_called()


def test_one_read_answers_every_check_within_the_hour() -> None:
    guard, read = guard_of("AAD_BASIC")
    for _ in range(3):
        with pytest.raises(LicenceRequired):
            guard.check(ConditionalAccessPolicy)
    assert read.call_count == ONE_READ


def test_a_read_is_repeated_once_the_hour_is_past() -> None:
    guard, read = guard_of("AAD_BASIC", ttl=0)
    for _ in range(2):
        with pytest.raises(LicenceRequired):
            guard.check(ConditionalAccessPolicy)
    assert read.call_count == TWO_READS


def test_any_one_of_the_named_plans_is_enough() -> None:
    guard, _ = guard_of("AAD_PREMIUM_P2")
    guard.check(TwoPlans)  # holding the second of the two is holding the family


def test_an_unreadable_tenant_is_unknown_and_never_blocks() -> None:
    read = unittest.mock.Mock(side_effect=PermissionError("Organization.Read.All was never granted"))
    guard = LicenceGuard(read=read, mode=ENFORCE)
    for _ in range(3):
        guard.check(ConditionalAccessPolicy)  # a guard that cannot see must not stop the call
    assert read.call_count == ONE_READ  # and a failed read is not retried on every call


def test_a_type_that_names_no_licence_is_asked_nothing() -> None:
    guard, read = guard_of()
    guard.check(User)
    read.assert_not_called()


def test_a_mode_that_is_not_one_of_the_three_is_refused_by_name() -> None:
    with pytest.raises(ValueError, match="O365_LICENCE_GUARD"):
        LicenceGuard(read=nothing, mode="strict")


def test_warn_names_the_missing_plan_and_lets_the_call_go() -> None:
    guard, _ = guard_of("AAD_BASIC", mode=WARN)
    with unittest.mock.patch("office365.licensing.guard.logger") as logger:
        guard.check(ConditionalAccessPolicy)
    assert "AAD_PREMIUM" in logger.warning.call_args[0][1]


def test_the_client_hands_its_guard_to_the_request_it_builds() -> None:
    client = GraphClient(tenant="contoso.onmicrosoft.com")
    # The direction of the dependency: a request is told what it may ask, never asks its client.
    assert client.pending_request()._licence_guard is client.licence_guard


def test_enforce_refuses_a_marked_call_before_a_token_is_asked_for() -> None:
    client = GraphClient(tenant="contoso.onmicrosoft.com")
    client._licence_guard = LicenceGuard(read=nothing, mode=ENFORCE)  # the tenant holds nothing
    # A missing token is a ValueError from the auth listener; getting the licence refusal instead
    # means the refusal came from building the request, which is before anything is sent.
    with pytest.raises(LicenceRequired, match="ConditionalAccessPolicy needs one of the licences AAD_PREMIUM"):
        client.policies.conditional_access_policies.get_all().execute_query()


def _query(target: type) -> ClientQuery[Any]:
    """A query that speaks for the given type, without needing a client to make one."""
    query: Any = unittest.mock.Mock()
    query.permission_requirement = None
    query.return_type, query.binding_type = target, target
    return query
