"""The join between a marker, the index and a tenant's subscriptions.

The index carries each noun's own marker, and ``subscribedSkus`` says what the tenant holds; this
file tests only what happens when the two meet - which seat is asked, what an unread seat says,
and that an answer of "no" is never guessed. What the real tree declares is asserted where the
markers are (``tests/unit/test_permission_vocabulary.py``) rather than restated here.
"""

import unittest

from office365 import cli
from office365.licensing.report import NO, UNKNOWN, YES, area_of, headline, of, products, rows
from office365.permissions.declaration import TENANT, USER


def _document(entries):
    """An index document with one product holding these ``(type ref, plans, seat)`` records."""
    return {
        "products": {
            "intune": {
                f"noun{position}": {
                    "noun": f"noun{position}",
                    "type": ref,
                    "licence": {"plans": list(plans), "seat": seat},
                }
                for position, (ref, plans, seat) in enumerate(entries)
            }
        }
    }


#: Two areas under one plan and seat, so grouping has something to do.
DOCUMENT = _document(
    [
        ("office365.intune.devices.managed.device:ManagedDevice", ("INTUNE_A",), TENANT),
        ("office365.intune.devices.managed.overview:ManagedDeviceOverview", ("INTUNE_A",), TENANT),
        ("office365.intune.policies.compliance:DeviceCompliancePolicy", ("INTUNE_A",), TENANT),
        ("office365.intune.devices.managed.seat:AssignedSeat", ("AAD_PREMIUM_P2",), USER),
    ]
)


class AreaTest(unittest.TestCase):
    def test_a_reference_names_the_package_it_lives_in(self):
        self.assertEqual(area_of("office365.intune.devices.management.managed.device:ManagedDevice"), "intune.devices")
        self.assertEqual(area_of("office365.directory.policies.conditional_access:Policy"), "directory.policies")


class DeclaredTest(unittest.TestCase):
    def test_one_plan_is_one_licence_over_the_areas_that_declare_it(self):
        (found,) = [item for item in of(DOCUMENT) if item.plans == ("INTUNE_A",)]
        self.assertEqual([family.name for family in found.families], ["intune.devices", "intune.policies"])
        self.assertEqual([family.nouns for family in found.families], [2, 1])
        self.assertEqual(found.nouns, 3)

    def test_a_plan_under_two_seats_is_two_answers(self):
        """The same plan is a different claim when the caller's own seat has to hold it."""
        self.assertEqual([item.seat for item in of(DOCUMENT)], [TENANT, USER])

    def test_the_one_that_opens_the_most_words_leads(self):
        self.assertEqual([item.name for item in of(DOCUMENT)], ["INTUNE_A", "AAD_PREMIUM_P2"])


def _answers(found):
    """The answer per seat, so a test asserts a fact rather than the order rows arrived in."""
    return {row["seat"]: row["held"] for row in found}


class HeldTest(unittest.TestCase):
    def test_a_tenant_seat_is_held_by_what_the_subscriptions_provision(self):
        self.assertEqual(_answers(rows(of(DOCUMENT), held=["INTUNE_A"]))[TENANT], YES)

    def test_a_plan_the_tenant_did_not_buy_is_not_held(self):
        found = rows(of(DOCUMENT), held=["TEAMS1"], mine=["AAD_PREMIUM_P2"])
        self.assertEqual(_answers(found), {TENANT: NO, USER: YES})

    def test_an_unread_seat_is_unknown_and_never_a_no(self):
        """A token without ``User.Read.All`` cannot answer, and must not accuse the tenant."""
        self.assertEqual(_answers(rows(of(DOCUMENT), held=["INTUNE_A"], mine=None)), {TENANT: YES, USER: UNKNOWN})

    def test_a_user_seat_asked_of_the_callers_own_licences(self):
        found = rows(of(DOCUMENT), held=["INTUNE_A", "AAD_PREMIUM_P2"], mine=["TEAMS1"])
        self.assertEqual(_answers(found), {TENANT: YES, USER: NO})

    def test_what_the_tenant_can_use_comes_first(self):
        found = rows(of(DOCUMENT), held=["INTUNE_A"], mine=None)
        self.assertEqual([row["held"] for row in found], [YES, UNKNOWN])


class ProductsTest(unittest.TestCase):
    def test_a_product_counts_its_words_and_those_that_name_a_licence(self):
        self.assertEqual(products(DOCUMENT), [{"product": "intune", "nouns": 4, "licensed": 4}])

    def test_a_product_that_needs_no_licence_still_names_its_words(self):
        """Zero licensed is a fact about the model, not about the tenant: no tenant is read."""
        document = {"products": {"admin": {"noun0": {"type": "office365.admin.exchange.client:Client"}}}}
        self.assertEqual(products(document), [{"product": "admin", "nouns": 1, "licensed": 0}])


class HeadlineTest(unittest.TestCase):
    def test_one_sentence_counts_the_licences_a_command_names(self):
        found = rows(of(DOCUMENT), held=["INTUNE_A"], mine=None)
        self.assertEqual(
            headline(found, "contoso.onmicrosoft.com"),
            "contoso.onmicrosoft.com: holds 1 of 2 licences a command names; 1 could not be read",
        )

    def test_without_a_tenant_it_still_answers(self):
        found = rows(of(DOCUMENT), held=["INTUNE_A", "AAD_PREMIUM_P2"], mine=["AAD_PREMIUM_P2"])
        self.assertEqual(headline(found), "holds all 2 licences a command names")

    def test_a_missing_plan_is_named_because_naming_it_is_the_whole_answer(self):
        found = rows(of(DOCUMENT), held=["INTUNE_A"], mine=[])
        self.assertEqual(headline(found), "holds 1 of 2 licences a command names; missing AAD_PREMIUM_P2")


class TableTest(unittest.TestCase):
    def test_a_default_table_counts_the_areas_a_plan_opens(self):
        """Eleven module names in a 48-column cell come out as `intune.…`; `11` says more."""
        records = rows(of(DOCUMENT), frozenset({"INTUNE_A"}), frozenset())

        printed = cli._licence_table(records, wide=False)

        self.assertIn("AREAS", printed)
        self.assertEqual([record["areas"] for record in records], [2, 1])
        self.assertNotIn("\u2026", printed)

    def test_wide_prints_each_area_on_the_line_it_belongs_to(self):
        """`intune.devices (2), intune.policies` in a cell is the paragraph wide must not print."""
        records = rows(of(DOCUMENT), frozenset({"INTUNE_A"}), frozenset())

        printed = cli._licence_table(records, wide=True)

        lines = printed.splitlines()

        self.assertEqual(printed.count("INTUNE_A"), 1)
        self.assertEqual(lines[0].split()[0], "INTUNE_A")
        self.assertTrue(any(line.startswith("  intune.devices") for line in lines))
        self.assertTrue(any(line.startswith("  intune.policies") for line in lines))
        self.assertNotIn("(2)", printed)
        self.assertNotIn("\u2026", printed)

    def test_a_column_that_says_yes_on_every_row_is_not_printed(self):
        """Under *holds all 4*, HELD is a header over nothing; the page keeps the fact once."""
        records = rows(of(DOCUMENT), frozenset({"INTUNE_A", "AAD_PREMIUM_P2"}), frozenset({"AAD_PREMIUM_P2"}))

        printed = cli._licence_table(records, wide=False)

        self.assertNotIn("HELD", printed)
        self.assertIn("AREAS", printed)
