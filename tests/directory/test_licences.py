"""Licences: the tenant's subscribed SKUs, and a user's license details."""

from __future__ import annotations

from office365.directory.licenses.details import LicenseDetails
from office365.directory.licenses.tenant import LicencesReport

from tests.graph_case import GraphDelegatedTestCase


class TestLicences(GraphDelegatedTestCase):
    report: LicencesReport

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.report = cls.client.licences.get_all().execute_query().value

    def test_subscribed_skus(self):
        skus = self.client.subscribed_skus.get().execute_query()
        self.assertEqual([sku.sku_id for sku in self.report.skus], [sku.sku_id for sku in skus])

    def test_sku_carries_its_provisioned_service_plans(self):
        for sku in self.report.skus:
            for plan in sku.service_plans:
                if plan.provisioningStatus == "Success" and plan.servicePlanName:
                    self.assertIn(plan.servicePlanName, self.report.plans)
                    self.assertIn(sku, self.report.carrying(plan.servicePlanName))

    def test_sku_without_enabled_seats_is_suspended(self):
        for sku in self.report.skus:
            if sku.capability_status in ("Suspended", "LockedOut", "Deleted"):
                self.assertIn(sku, self.report.suspended)

    def test_spare_seats_are_unassigned(self):
        for sku in self.report.skus:
            spare = (sku.consumed_units or 0) < (sku.prepaid_units.enabled or 0)
            self.assertEqual(sku in self.report.unassigned, spare)

    def test_user_license_details(self):
        me = self.client.me.get().execute_query()
        mine = self.client.licences.get_user(me).execute_query().value
        by_name = self.client.licences.get_user(me.user_principal_name).execute_query().value
        self.assertEqual([licence.sku_id for licence in mine.skus], [licence.sku_id for licence in by_name.skus])
        for licence in mine.skus:
            self.assertIsInstance(licence, LicenseDetails)
