"""Two service roots, one model: which root a suite addresses, and what that buys it.

The version is a property of the *request*, not of the model. A suite therefore names the root
it means by naming the client - ``self.client`` for ``v1.0``, ``self.client_beta`` for ``beta``
(see :mod:`tests.graph_case`) - and neither name is a mode the other inherits.

What this file pins is the consequence: the same member answers from either root, while a
member only the beta metadata declares is refused by the stable one *before* it is sent
(``NotSupportedInVersion``). That refusal is the interesting half. Graph's answer to
``GET /v1.0/deviceManagement/intents`` is a 404 that reads like a typo in a URL; the model
knows the difference between "this path does not exist" and "this root has no such member",
and the error it raises is the one a caller can act on.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.graph_version import GraphVersion
from office365.intune.devices.management.intent import DeviceManagementIntent
from office365.intune.devices.management.managed.collection import ManagedDeviceCollection
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly import (
    UserExperienceAnalyticsAnomaly,
)
from office365.runtime.types.odata_property import NotSupportedInVersion

from tests.decorators import requires_delegated
from tests.intune.intune_case import MANAGED_DEVICES, IntuneCase


class TestTheServiceRoot(IntuneCase):
    """`GraphVersion` selects the root a client addresses."""

    def test_01_the_default_client_addresses_the_stable_root(self):
        """A suite that says nothing addresses v1.0."""
        self.assertEqual(GraphVersion.default(), GraphVersion.V1)
        self.assertEqual(self.client.pending_request().service_root_url, "https://graph.microsoft.com/v1.0")

    def test_02_the_beta_client_addresses_the_beta_root(self):
        """`client_beta` is the same suite's credentials, on the other root."""
        self.assertEqual(self.client_beta.pending_request().service_root_url, "https://graph.microsoft.com/beta")
        self.assertIsNot(self.client_beta, self.client)

    def test_03_the_version_is_read_from_the_pending_request(self):
        """`client.version` reports what the request will address, and follows a write."""
        client = self.sign_in(GraphVersion.V1)  # a private client: the write below must not leak
        self.assertTrue(client.version.is_stable)

        client.version = GraphVersion.BETA
        self.assertTrue(client.version.is_beta)
        self.assertEqual(client.pending_request().service_root_url, "https://graph.microsoft.com/beta")

    @requires_delegated(*MANAGED_DEVICES)
    def test_04_the_same_member_answers_from_either_root(self):
        """A managed-device read succeeds on both roots: the model is shared, the address is not."""
        for client in (self.client, self.client_beta):
            result = client.device_management.managed_devices.get().execute_query()

            self.assertIsInstance(result, ManagedDeviceCollection)
            self.assertTrue(str(result.resource_path).endswith("/managedDevices"))

    @requires_delegated(*MANAGED_DEVICES)
    def test_05_a_preview_member_is_refused_by_the_stable_root(self):
        """`deviceManagement.intents` is beta-only, and the refusal happens before the wire."""
        with self.assertRaises(NotSupportedInVersion) as refused:
            _ = self.dm.intents

        self.assertIn("intents", str(refused.exception))
        self.assertIn("beta", str(refused.exception))

    @requires_delegated(*MANAGED_DEVICES)
    def test_06_and_served_by_the_preview_root(self):
        """The same member on beta is a collection, and reads as one."""
        rows = self.dm_beta.intents.top(5).get().execute_query()

        self.assertIsInstance(rows, EntityCollection)
        self.assertTrue(str(rows.resource_path).endswith("/deviceManagement/intents"))
        if len(rows):
            self.assertIsInstance(rows[0], DeviceManagementIntent)

    def test_07_the_analytics_family_arrived_beta_only(self):
        """The whole `userExperienceAnalytics*` subtree is absent from `Graph.xml`, so it is gated.

        Nothing is sent: the gate is read off the metadata snapshots, which is why this needs no
        grant and no row. Both halves are asserted - the getter the caller reaches for, and the
        class it would otherwise build from the stable root's context.
        """
        with self.assertRaises(NotSupportedInVersion) as refused:
            _ = self.dm.user_experience_analytics_anomaly
        self.assertIn("userExperienceAnalyticsAnomaly", str(refused.exception))

        with self.assertRaises(NotSupportedInVersion):
            UserExperienceAnalyticsAnomaly(self.client)
