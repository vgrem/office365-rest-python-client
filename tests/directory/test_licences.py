"""Licences — the three questions a caller actually asks.

What has this tenant bought, what does one user hold, and which of those seats is going unused.
Each answer is a read of the tenant's own inventory (``subscribedSkus``, ``licenseDetails``), so
every assertion is made against what the service returned rather than against a fixture.
"""

from __future__ import annotations

from office365.directory.licenses.details import LicenseDetails
from office365.directory.licenses.tenant import LicenceManager, LicencesReport

from tests.graph_case import GraphDelegatedTestCase


class TestTenantLicences(GraphDelegatedTestCase):
    """``client.licences``, answered from the models the service returned."""

    held: LicencesReport

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.held = cls.client.licences.get_all().execute_query().value

    def test_the_tenant_licences_are_what_subscribed_skus_lists(self):
        listed = self.client.subscribed_skus.get().execute_query()
        self.assertTrue(len(listed) > 0, "a tenant with no subscribed SKU cannot answer a licence question")
        self.assertEqual([sku.sku_part_number for sku in self.held.skus], [sku.sku_part_number for sku in listed])

    def test_a_licence_names_the_plans_it_turns_on(self):
        provisioned = {
            plan.servicePlanName
            for sku in self.held.skus
            for plan in sku.service_plans
            if plan.provisioningStatus == "Success" and plan.servicePlanName
        }
        self.assertEqual(self.held.plans, frozenset(provisioned))
        for name in list(self.held.plans)[:5]:
            self.assertIn(name, self.held.names)
            self.assertTrue(self.held.carrying(name))

    def test_a_seat_nobody_uses_is_reported_spare(self):
        for sku in self.held.skus:
            spare = (sku.consumed_units or 0) < (sku.prepaid_units.enabled or 0)
            self.assertEqual(sku in self.held.unassigned, spare)

    def test_the_plan_id_is_the_join_key_an_assignment_uses(self):
        for sku in self.held.skus:
            for plan in sku.service_plans:
                if plan.provisioningStatus == "Success" and plan.servicePlanName:
                    self.assertEqual(self.held.plan_id(plan.servicePlanName), plan.servicePlanId)
                    self.assertEqual(self.held.plan_name(plan.servicePlanId or ""), plan.servicePlanName)
                    return
        self.skipTest("no provisioned plan to join")

    def test_my_licences_are_my_assignments_not_the_tenants_seats(self):
        mine = self.client.licences.get_user(self.client.me).execute_query().value
        for licence in mine.skus:
            self.assertIsInstance(licence, LicenseDetails)
            self.assertIn(licence.sku_id, {sku.sku_id for sku in self.held.skus})
        self.assertEqual(mine.unassigned, ())

    def test_another_users_licences_are_read_by_principal_name(self):
        me = self.client.me.get().execute_query()
        by_name = self.client.licences.get_user(me.user_principal_name).execute_query().value
        by_entity = self.client.licences.get_user(me).execute_query().value
        self.assertEqual([licence.sku_id for licence in by_name.skus], [licence.sku_id for licence in by_entity.skus])

    def test_reaching_the_manager_sends_nothing(self):
        self.assertIsInstance(self.client.licences, LicenceManager)

    def test_a_read_is_not_kept(self):
        again = self.client.licences.get_all().execute_query().value
        self.assertIsNot(again, self.held)
        self.assertEqual([sku.sku_id for sku in again.skus], [sku.sku_id for sku in self.held.skus])
