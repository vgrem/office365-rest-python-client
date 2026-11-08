"""What counts as a licence name, and what a name is worth.

The names are the vocabulary a requirement asks in: a SKU part number is packaging, a service
plan is capability, and a plan the tenant has not provisioned is not held yet.
"""

from __future__ import annotations

import unittest

from office365.directory.licenses.details import LicenseDetails
from office365.directory.licenses.service_plan_info import ServicePlanInfo
from office365.directory.licenses.tenant import Licences
from office365.runtime.client_value_collection import ClientValueCollection


def _details(part_number: str, *plans: ServicePlanInfo) -> LicenseDetails:
    """A licence as the wire delivers it: one SKU part number and the plans inside it."""
    details = LicenseDetails(None)
    details.set_property("skuPartNumber", part_number)
    details.set_property("servicePlans", ClientValueCollection(ServicePlanInfo, list(plans)))
    return details


class TestLicenceNames(unittest.TestCase):
    def test_a_name_is_the_sku_and_the_plans_it_provisioned(self):
        licences = Licences(
            [
                _details(
                    "ENTERPRISEPACK",
                    ServicePlanInfo(servicePlanName="EXCHANGE_S_ENTERPRISE", provisioningStatus="Success"),
                )
            ]
        )
        self.assertEqual(licences.names, {"ENTERPRISEPACK", "EXCHANGE_S_ENTERPRISE"})

    def test_a_plan_the_tenant_did_not_provision_is_not_held(self):
        licences = Licences(
            [
                _details(
                    "M365_E5",
                    ServicePlanInfo(servicePlanName="RECORDS_MANAGEMENT", provisioningStatus="PendingProvisioning"),
                )
            ]
        )
        self.assertFalse(licences.holds("RECORDS_MANAGEMENT"))
        self.assertTrue(licences.holds("M365_E5"))

    def test_carrying_names_the_product_that_turns_a_plan_on(self):
        licences = Licences(
            [
                _details(
                    "SPE_E3", ServicePlanInfo(servicePlanName="EXCHANGE_S_ENTERPRISE", provisioningStatus="Success")
                ),
                _details("M365_E5", ServicePlanInfo(servicePlanName="RECORDS_MANAGEMENT", provisioningStatus="Success")),
            ]
        )
        self.assertEqual([sku.sku_part_number for sku in licences.carrying("RECORDS_MANAGEMENT")], ["M365_E5"])

    def test_a_requirement_may_name_any_of_the_seats_that_satisfy_it(self):
        licences = Licences([_details("DEVELOPERPACK_E5")])
        self.assertTrue(licences.holds("SPE_E5", "DEVELOPERPACK_E5"))
        self.assertFalse(licences.holds("SPE_E5", "M365_E5"))
