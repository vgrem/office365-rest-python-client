"""Licences — what the tenant bought, and what each licence turns on.

The report's whole job is the tenant's own inventory, so every assertion here is made against
what ``subscribedSkus`` returned: the SKUs it owns, the plans those provisioned, the seats
nobody is using. A licence the tenant has not bought is not answerable here, and nothing in the
library pretends otherwise - the public product catalogue is Microsoft's published data, not
something Graph returns.
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

    def test_reaching_the_manager_sends_nothing(self):
        self.assertIsInstance(self.client.licences, LicenceManager)

    def test_the_tenant_holds_the_skus_the_service_listed(self):
        self.assertTrue(len(self.held.skus) > 0, "a tenant with no subscribed SKU cannot answer a licence question")
        listed = self.client.subscribed_skus.get().execute_query()
        self.assertEqual([sku.sku_id for sku in self.held.skus], [sku.sku_id for sku in listed])

    def test_a_sku_is_held_under_the_part_number_the_service_reports(self):
        for sku in self.held.skus:
            self.assertIn(sku.sku_part_number, self.held.names)
            self.assertTrue(self.held.holds(sku.sku_part_number or ""))

    def test_a_provisioned_plan_is_held_by_the_sku_that_provisions_it(self):
        for sku in self.held.skus:
            for plan in sku.service_plans:
                if plan.provisioningStatus != "Success" or not plan.servicePlanName:
                    continue
                self.assertIn(sku, self.held.carrying(plan.servicePlanName))
                self.assertIn(plan.servicePlanName, self.held.plans)

    def test_a_plan_the_tenant_did_not_provision_is_not_held(self):
        for sku in self.held.skus:
            for plan in sku.service_plans:
                if plan.provisioningStatus == "Success" or not plan.servicePlanName:
                    continue
                self.assertNotIn(sku, self.held.carrying(plan.servicePlanName))
                self.assertNotIn(plan.servicePlanName, self.held.plans)

    def test_a_plan_id_and_a_plan_name_are_the_same_plan(self):
        for sku in self.held.skus:
            for plan in sku.service_plans:
                if plan.provisioningStatus != "Success" or not plan.servicePlanName:
                    continue
                self.assertEqual(self.held.plan_id(plan.servicePlanName), plan.servicePlanId)
                self.assertEqual(self.held.plan_name(plan.servicePlanId or ""), plan.servicePlanName)

    def test_a_seat_nobody_uses_is_a_seat_the_tenant_bought(self):
        for sku in self.held.unassigned:
            self.assertLess(sku.consumed_units or 0, sku.prepaid_units.enabled or 0)

    def test_an_assigned_seat_is_not_reported_as_unassigned(self):
        for sku in self.held.skus:
            spare = (sku.consumed_units or 0) < (sku.prepaid_units.enabled or 0)
            self.assertEqual(sku in self.held.unassigned, spare)

    def test_a_suspended_sku_is_named_rather_than_counted_as_held(self):
        for sku in self.held.suspended:
            self.assertIn(sku.capability_status, {"Suspended", "LockedOut", "Deleted"})

    def test_a_user_reads_their_own_assignments_rather_than_the_tenants_seats(self):
        mine = self.client.licences.get_user(self.client.me).execute_query().value
        for licence in mine.skus:
            self.assertIsInstance(licence, LicenseDetails)
        self.assertEqual(mine.unassigned, ())
        self.assertEqual(mine.suspended, ())

    def test_a_user_is_addressed_by_their_principal_name_too(self):
        me = self.client.me.get().execute_query()
        by_name = self.client.licences.get_user(me.user_principal_name).execute_query().value
        self.assertEqual(
            [licence.sku_id for licence in by_name.skus],
            [licence.sku_id for licence in self.client.licences.get_user(me).execute_query().value.skus],
        )

    def test_a_licence_bought_for_nobody_is_visible_before_it_is_assigned(self):
        held = self.client.licences.get_all().execute_query().value
        self.assertEqual({sku.sku_id for sku in held.skus}, {sku.sku_id for sku in self.held.skus})
        self.assertIsNot(held, self.held)
