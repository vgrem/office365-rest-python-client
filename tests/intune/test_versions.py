"""The service root a Graph client addresses, and Intune on the preview root.

Deliberately not covered here: a preview-only capability. `office365.intune` has no member
whose segment `v1.0` does not carry, so nothing in this file can prove that a beta-only
family exists — the shipped model is the `v1.0` shape, and `beta` is a superset of it.
These tests pin the addressing instead: the version is a property of the client's request
(not of the model), so the same member has to answer from whichever root the client
addresses.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.intune.devices.management.managed.collection import ManagedDeviceCollection
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase
from tests.settings import settings


class TestTheServiceRoot(GraphDelegatedTestCase):
    """`GraphVersion` selects the root a client addresses."""

    beta: GraphClient = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.beta = GraphClient(tenant=settings.tenant, version=GraphVersion.BETA).with_username_and_password(
            settings.client_id, settings.username, settings.password
        )

    def test_01_a_client_addresses_the_root_it_was_given(self):
        """The default client addresses the stable root; an explicit one addresses beta."""
        self.assertEqual(GraphVersion.default(), GraphVersion.V1)
        self.assertEqual(self.client.pending_request().service_root_url, "https://graph.microsoft.com/v1.0")
        self.assertEqual(self.beta.pending_request().service_root_url, "https://graph.microsoft.com/beta")

    def test_02_the_version_is_read_from_the_pending_request(self):
        """`client.version` reports what the request will address, and follows a write."""
        self.assertTrue(self.client.version.is_stable)
        self.assertTrue(self.beta.version.is_beta)

        self.beta.version = GraphVersion.V1
        self.assertEqual(self.beta.pending_request().service_root_url, "https://graph.microsoft.com/v1.0")
        self.beta.version = GraphVersion.BETA

    @requires_delegated(
        "DeviceManagementManagedDevices.Read.All",
        "DeviceManagementManagedDevices.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_03_the_same_member_answers_from_either_root(self):
        """A managed-device read succeeds on both roots: the model is shared, the address is not."""
        for client in (self.client, self.beta):
            result = client.device_management.managed_devices.get().execute_query()
            self.assertIsInstance(result, ManagedDeviceCollection)
            self.assertTrue(str(result.resource_path).endswith("/managedDevices"))
