"""The families that hold a secret: PFX certificates, local-admin passwords, connectors.

None of these has a ``v1.0`` counterpart, so each read goes through the beta client and the
stable root's refusal is asserted rather than assumed - a family that quietly started
answering on ``v1.0`` would mean the two snapshots had converged, which is a fact worth
noticing here before it is noticed in production.

What they have in common is that the tenant has to be enrolled and licensed for a connector
to exist at all, and the test tenant is not, so the reads mostly answer with nothing: the wire
and the item type are the assertion, and the row - when there is one - is read for the
property the family exists for.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.devices.management.certificate_connector_details import CertificateConnectorDetails
from office365.intune.devices.management.hardware_password_info import HardwarePasswordInfo
from office365.intune.devices.management.managed.ebook.e_book_category import ManagedEBookCategory
from office365.intune.devices.management.symantec_code_signing_certificate import SymantecCodeSigningCertificate
from office365.intune.devices.management.user_pfx_certificate import UserPFXCertificate
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.types.odata_property import NotSupportedInVersion

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

CONFIGURATION = (
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementConfiguration.ReadWrite.All",
)

APPS = (
    "DeviceManagementApps.Read.All",
    "DeviceManagementApps.ReadWrite.All",
)


class TestCertificates(GraphDelegatedTestCase):
    """`userPfxCertificates`, `certificateConnectorDetails` and the Symantec certificate."""

    @requires_delegated(*CONFIGURATION)
    def test_01_a_pfx_certificate_is_a_beta_collection(self):
        """`GET /beta/deviceManagement/userPfxCertificates` yields `UserPFXCertificate` rows."""
        certificates = self.client_beta.device_management.user_pfx_certificates
        self.assertTrue(str(certificates.resource_path).endswith("/userPfxCertificates"))

        rows = certificates.top(5).get().execute_query()

        self.assertIsInstance(rows, EntityCollection)
        self.assertIs(rows._item_type, UserPFXCertificate)
        if len(rows):
            self.assertIsInstance(rows[0], UserPFXCertificate)
            self.assertIsNone(rows[0].get_property("encryptedPfxBlob", None))

    @requires_delegated(*CONFIGURATION)
    def test_02_a_certificate_connector_is_declared_as_a_collection_the_service_does_not_route(self):
        """Measured: the CSDL says `Collection(graph.certificateConnectorDetails)`, the service says 400.

        Graph answers ``"No method match route template ... for request
        .../deviceManagement/certificateConnectorDetails"``: it routes ``deviceManagement`` as a
        singleton and publishes no ``GET`` for this navigation, so there is no collection
        endpoint today. The model follows the schema it was generated from, and this pins the
        gap - if Graph grows the route, the failure here says the quirk is gone rather than
        letting a test silently start passing for a different reason.
        """
        connectors = self.client_beta.device_management.certificate_connector_details
        self.assertIs(connectors._item_type, CertificateConnectorDetails)
        self.assertTrue(str(connectors.resource_path).endswith("/deviceManagement/certificateConnectorDetails"))

        with self.assertRaises(ClientRequestException) as refused:
            connectors.top(1).get().execute_query()
        self.assertIn("No method match route template", str(refused.exception))

    @requires_delegated(*CONFIGURATION)
    def test_03_the_symantec_certificate_is_one_entity_not_a_collection(self):
        """`symantecCodeSigningCertificate` is the tenant's single certificate, on `deviceAppManagement`."""
        certificate = self.client_beta.device_app_management.symantec_code_signing_certificate

        self.assertIsInstance(certificate, SymantecCodeSigningCertificate)
        self.assertTrue(str(certificate.resource_path).endswith("/deviceAppManagement/symantecCodeSigningCertificate"))
        self.assertIn("content", SymantecCodeSigningCertificate._schema.properties)


class TestPasswordsAndEbooks(GraphDelegatedTestCase):
    """Two misnamed families: `hardwarePasswordInfo` is a collection, `managedEBookCategories` a tree."""

    @requires_delegated("DeviceManagementManagedDevices.PrivilegedOperations.All")
    def test_04_a_local_admin_password_is_read_only(self):
        """LAPS for Intune: the password is readable and never posted back."""
        passwords = self.client_beta.device_management.hardware_password_info
        self.assertTrue(str(passwords.resource_path).endswith("/hardwarePasswordInfo"))

        rows = passwords.top(5).get().execute_query()

        self.assertIs(rows._item_type, HardwarePasswordInfo)
        self.assertIn("currentPassword", HardwarePasswordInfo._schema.readonly)
        if len(rows):
            self.assertIsInstance(rows[0], HardwarePasswordInfo)

    @requires_delegated(*APPS)
    def test_05_an_ebook_category_hangs_off_app_management(self):
        """`managedEBookCategories` classifies the e-books `managedEBooks` publishes."""
        categories = self.client_beta.device_app_management.managed_e_book_categories
        self.assertTrue(str(categories.resource_path).endswith("/managedEBookCategories"))

        rows = categories.top(5).get().execute_query()

        self.assertIs(rows._item_type, ManagedEBookCategory)
        if len(rows):
            self.assertIsInstance(rows[0], ManagedEBookCategory)

    def test_06_the_stable_root_refuses_every_one_of_them(self):
        """Beta-only is a property of the member, and the refusal names it before it is sent."""
        for name, member in [
            ("userPfxCertificates", lambda: self.client.device_management.user_pfx_certificates),
            ("hardwarePasswordInfo", lambda: self.client.device_management.hardware_password_info),
            ("managedEBookCategories", lambda: self.client.device_app_management.managed_e_book_categories),
        ]:
            with self.subTest(member=name):
                with self.assertRaises(NotSupportedInVersion) as refused:
                    member()
                self.assertIn(name, str(refused.exception))
