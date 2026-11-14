"""The families that hold a secret: PFX certificates, local-admin passwords, connectors.

None of these has a ``v1.0`` counterpart, so each read goes through ``self.dm_beta`` and the
stable root's refusal is asserted rather than assumed - a family that quietly started
answering on ``v1.0`` would mean the two snapshots had converged, which is a fact worth
noticing here before it is noticed in production.

What they have in common is that the tenant has to be enrolled and licensed for a connector
to exist at all, and the test tenant is not, so the reads mostly answer with nothing. That is
why the guard is ``row_or_skip``: the wire and the item type are the assertion, and the row -
when there is one - is read for the property the family exists for.
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
from tests.intune.intune_case import APPS, CONFIGURATION, PRIVILEGED_OPERATIONS, IntuneCase


class TestCertificates(IntuneCase):
    """`userPfxCertificates`, `certificateConnectorDetails` and the Symantec certificate."""

    @requires_delegated(*CONFIGURATION)
    def test_01_a_pfx_certificate_is_a_beta_collection(self):
        """`GET /beta/deviceManagement/userPfxCertificates` yields `UserPFXCertificate` rows."""
        rows = self.read(self.dm_beta.user_pfx_certificates, "userPfxCertificates")

        self.assertIsInstance(rows, EntityCollection)
        self.assertIs(rows._item_type, UserPFXCertificate)
        row = self.row_or_skip(rows, "user PFX certificate")
        self.assertIsInstance(row, UserPFXCertificate)
        self.assertIsNone(row.get_property("encryptedPfxBlob", None))

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
        collection = self.dm_beta.certificate_connector_details

        self.assertIs(collection._item_type, CertificateConnectorDetails)
        self.assertTrue(str(collection.resource_path).endswith("/deviceManagement/certificateConnectorDetails"))
        with self.assertRaises(ClientRequestException) as refused:
            collection.top(1).get().execute_query()
        self.assertIn("No method match route template", str(refused.exception))

    @requires_delegated(*CONFIGURATION)
    def test_03_the_symantec_certificate_is_one_entity_not_a_collection(self):
        """`symantecCodeSigningCertificate` is the tenant's single certificate, on `deviceAppManagement`."""
        certificate = self.client_beta.device_app_management.symantec_code_signing_certificate

        self.assertIsInstance(certificate, SymantecCodeSigningCertificate)
        self.assertTrue(str(certificate.resource_path).endswith("/deviceAppManagement/symantecCodeSigningCertificate"))
        self.assertIn("content", SymantecCodeSigningCertificate._schema.properties)


class TestPasswordsAndEbooks(IntuneCase):
    """Two misnamed families: `hardwarePasswordInfo` is a collection, `managedEBookCategories` a tree."""

    @requires_delegated(*PRIVILEGED_OPERATIONS)
    def test_04_a_local_admin_password_is_read_only(self):
        """LAPS for Intune: the password is readable and never posted back."""
        rows = self.read(self.dm_beta.hardware_password_info, "hardwarePasswordInfo")

        self.assertIs(rows._item_type, HardwarePasswordInfo)
        self.assertIn("currentPassword", HardwarePasswordInfo._schema.readonly)
        row = self.row_or_skip(rows, "hardware password")
        self.assertIsInstance(row, HardwarePasswordInfo)

    @requires_delegated(*APPS)
    def test_05_an_ebook_category_hangs_off_app_management(self):
        """`managedEBookCategories` classifies the e-books `managedEBooks` publishes."""
        rows = self.read(self.client_beta.device_app_management.managed_e_book_categories, "managedEBookCategories")

        self.assertIs(rows._item_type, ManagedEBookCategory)
        row = self.row_or_skip(rows, "managed e-book category")
        self.assertIsInstance(row, ManagedEBookCategory)

    def test_06_the_stable_root_refuses_every_one_of_them(self):
        """Beta-only is a property of the member, and the refusal names it before it is sent."""
        for name, member in [
            ("userPfxCertificates", lambda: self.dm.user_pfx_certificates),
            ("hardwarePasswordInfo", lambda: self.dm.hardware_password_info),
            ("managedEBookCategories", lambda: self.client.device_app_management.managed_e_book_categories),
        ]:
            with self.assertRaises(NotSupportedInVersion) as refused:
                member()
            self.assertIn(name, str(refused.exception))
