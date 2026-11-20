"""A licence is a fact about a capability, so the model states it once, above the class.

Two markers, one vocabulary: ``@requires_license`` on a type says what the family needs to exist
at all, and ``licenses=`` on ``@require_permission`` says when one call is narrower than its
family. Both name *service plan names* - the ones a tenant's ``subscribedSkus`` already carries -
because a SKU part number is packaging and the plan is the capability inside it.

The tests below hold the three things that can silently rot: the marker being read back (a class,
its subclass, a member), the two sources being unioned rather than one shadowing the other, and
the names belonging to a closed set - a typo here would tell a caller to buy something that does
not exist, and no request would ever reveal it.
"""

from __future__ import annotations

import pathlib
import re

import pytest
from office365.capabilities import capabilities_of, hints_of
from office365.cli import _page
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.directory.protection.riskyusers.risky_user import RiskyUser
from office365.directory.rolemanagement.unifiedrole.assignment import UnifiedRoleAssignment
from office365.directory.rolemanagement.unifiedrole.schedule_base import UnifiedRoleScheduleBase
from office365.entity import Entity
from office365.intune.devices.management.managed.device import ManagedDevice
from office365.permissions.declaration import declared, licenses_of, require_permission, requires_license
from office365.routing import route
from office365.search.entity import SearchEntity
from office365.sharepoint.webs.web import Web

#: The licence names a marker may use, and the capability each one buys. Closed on purpose: a
#: name that is not here is a typo or an undeclared decision, and both should stop the build
#: rather than reach a user as advice to buy something that does not exist.
#:
#: A service plan is the vocabulary - it is what ``subscribedSkus`` reports and what a
#: requirement can be checked against. The one SKU part number below is the exception that
#: proves the rule: `search/entity.py` says an E5-class seat is enough without naming which
#: plan inside it grants Microsoft Search, so the packaging is recorded here, visibly, instead
#: of being dropped or guessed at.
SERVICE_PLANS = {
    "AAD_PREMIUM": "Entra ID P1 - conditional access, group-based licensing",
    "AAD_PREMIUM_P2": "Entra ID P2 - identity protection, PIM, access reviews",
    "INTUNE_A": "Microsoft Intune - device and app management",
    "RECORDS_MANAGEMENT": "Purview records management - retention labels and file plan",
    "THREAT_INTELLIGENCE": "Defender threat intelligence - indicators and TI APIs",
    "SPE_E5": "Microsoft 365 E5 (a SKU, not a plan) - the seat that includes search",
}

#: The families whose licence is not a judgement call: the feature is the licence. Kept as a
#: table so removing a marker is a red test rather than a quiet loss of a warning.
LICENSED_FAMILIES = (
    (ConditionalAccessPolicy, ("AAD_PREMIUM",)),
    (RiskyUser, ("AAD_PREMIUM_P2",)),
    (UnifiedRoleScheduleBase, ("AAD_PREMIUM_P2",)),
    (ManagedDevice, ("INTUNE_A",)),
)

#: Where the package's own source lives, scanned as text so a typo is caught without importing
#: 2,000 modules and without a tenant to ask.
PACKAGE = pathlib.Path(__file__).resolve().parents[2] / "office365"

#: A service plan name: SHOUTING_SNAKE, always at least two characters.
PLAN_NAME = re.compile(r"^[A-Z][A-Z0-9_]+$")

#: The two spellings a licence takes in source, and the names inside each.
STAMPED = re.compile(r"requires_license\(\s*([^)]*)\)")
NARROWED = re.compile(r"licenses=\s*\[([^\]]*)\]")


@pytest.mark.parametrize(("family", "plans"), LICENSED_FAMILIES)
def test_a_family_declares_what_it_takes_to_exist(family: type, plans: tuple[str, ...]) -> None:
    assert licenses_of(family) == plans


def test_a_reader_of_a_licensed_family_needs_no_licence_of_its_own() -> None:
    # The membership itself is granted without PIM, so it answers with nothing: the marker is on
    # the schedule types, not on the role assignment they sit beside.
    assert licenses_of(UnifiedRoleAssignment) == ()


def test_a_type_that_takes_nothing_declares_nothing() -> None:
    assert licenses_of(Web) == ()


def test_a_subclass_inherits_the_family_licence_and_may_restate_it() -> None:
    @requires_license("AAD_PREMIUM")
    class Base(Entity):
        pass

    class Child(Base):
        pass

    @requires_license("AAD_PREMIUM_P2")
    class Narrower(Base):
        pass

    assert licenses_of(Base) == ("AAD_PREMIUM",)
    assert licenses_of(Child) == ("AAD_PREMIUM",)
    assert licenses_of(Narrower) == ("AAD_PREMIUM_P2",)


def test_a_member_answers_with_the_licence_of_the_class_that_spells_it() -> None:
    # `restore` is declared on the class itself, so its qualified name resolves back to it.
    assert licenses_of(ConditionalAccessPolicy.restore) == ("AAD_PREMIUM",)


def test_an_empty_marker_is_refused_at_import_time() -> None:
    with pytest.raises(ValueError, match="names no plan"):
        requires_license()


def test_a_narrowing_declaration_wins_over_the_family_and_both_are_reported() -> None:
    @requires_license("AAD_PREMIUM")
    class _Family(Entity):
        @require_permission(delegated=["Policy.Read.All"])
        def read(self) -> None: ...

        @require_permission(delegated=["Policy.Read.All"], licenses=["AAD_PREMIUM_P2"])
        def narrow(self) -> None: ...

    capabilities = capabilities_of(_Family)
    assert capabilities.declarations["read"].licenses == ("AAD_PREMIUM",)
    assert capabilities.declarations["narrow"].licenses == ("AAD_PREMIUM_P2",)
    assert declared(_Family.read).licenses == ()
    assert capabilities.licenses == ("AAD_PREMIUM", "AAD_PREMIUM_P2")


def test_a_hint_names_the_licence_even_when_no_permission_is_declared() -> None:
    hints = hints_of(ManagedDevice, _undeclared_verb(ManagedDevice))
    assert "Needs one of these licences: INTUNE_A." in hints


def test_a_declaring_member_carries_the_family_licence_in_its_own_sentence() -> None:
    # 20 of the type's verbs declare a permission and none of them names a licence, so the
    # family's mark has to reach them - otherwise the page would say what to grant and stay
    # silent about the seat that has to be bought first.
    capabilities = capabilities_of(ManagedDevice)
    method = next(name for name in capabilities.declarations if name in capabilities.verbs)
    assert capabilities.declarations[method].licenses == ("INTUNE_A",)
    assert "one of the licences INTUNE_A" in hints_of(ManagedDevice, method)[0]


def test_a_hint_names_a_licence_once_even_though_two_sources_know_it() -> None:
    # `query` names SPE_E5 itself and the union reports it as well; the page must read as one
    # fact, not two lines saying the same plan twice.
    hints = hints_of(SearchEntity, "query")
    assert sum(line.count("SPE_E5") for line in hints) == 1


def test_the_page_says_what_a_family_needs_once_not_once_per_action() -> None:
    page = _page("intune", "managed-device", route("intune", "managed-device"))
    assert "  needs a licence: INTUNE_A" in page.split("\n")
    assert page.count("INTUNE_A") == 1


def test_every_stamped_name_is_a_licence_marker_can_name() -> None:
    stamped = _names_for(STAMPED) | _names_for(NARROWED)
    assert stamped, "no licence marker found: the scan is looking in the wrong place"
    assert stamped <= set(SERVICE_PLANS), f"unknown licence name: {sorted(stamped - set(SERVICE_PLANS))}"
    for name in stamped:
        assert PLAN_NAME.match(name), name


def _undeclared_verb(target: type) -> str:
    """One verb the type declares without a permission, so a hint can be asked for it alone."""
    capabilities = capabilities_of(target)
    return next(name for name in sorted(capabilities.verbs) if name not in capabilities.declarations)


def _names_for(pattern: re.Pattern[str]) -> set[str]:
    """Every licence name written in the package's source with this spelling."""
    found: set[str] = set()
    for path in PACKAGE.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for group in pattern.findall(text):
            found.update(re.findall(r"[\"']([A-Z][A-Z0-9_]+)[\"']", group))
    return found
