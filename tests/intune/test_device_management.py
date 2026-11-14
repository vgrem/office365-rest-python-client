"""``deviceManagement``: the tenant's Intune root, its singletons, and the plain lists.

Measured on the test tenant: Intune is *licensed* but not *provisioned* for the caller -
``subscriptionState`` answers ``pending`` and ``settings`` comes back null - so the objects that
describe a deployment are asserted as nullable here, and only their shape when present. An
empty collection is a fact about the tenant, not a failure of the call.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.devices.management.management import DeviceManagement
from office365.intune.devices.management.subscriptionstate import (
    DeviceManagementSubscriptionState,
)

from tests.decorators import requires_delegated
from tests.intune.intune_case import APPS, CONFIGURATION, IntuneCase


class TestDeviceManagementRoot(IntuneCase):
    """The object every Intune member hangs off, on both roots."""

    @requires_delegated(*CONFIGURATION)
    def test_01_the_root_object_answers_for_the_tenant(self):
        """``GET deviceManagement`` returns one object, and its state is an enum, not a string."""
        dm = self.dm.get().execute_query()

        self.assertIsInstance(dm, DeviceManagement)
        self.assertTrue(str(dm.resource_path).endswith("/deviceManagement"))
        self.assertIsInstance(dm.subscription_state, DeviceManagementSubscriptionState)

    @requires_delegated(*CONFIGURATION)
    def test_02_the_deployment_settings_arrive_only_when_intune_is_activated(self):
        """``settings`` is the tenant's Intune deployment, and null until it exists."""
        dm = self.dm.get().execute_query()

        if dm.settings is None:
            self.assertIsNot(
                dm.subscription_state,
                DeviceManagementSubscriptionState.active,
                "an active Intune subscription must carry deployment settings",
            )
            self.skipTest(f"Intune is not activated here (subscriptionState: {dm.subscription_state.name})")

        self.assertIsNotNone(dm.settings.get_property("id"))

    @requires_delegated(*CONFIGURATION)
    def test_03_the_state_summaries_are_singletons_not_collections(self):
        """The per-tenant state summaries are objects: they carry no ``/`` to address a row."""
        for name in ("device_configuration_device_state_summaries", "device_compliance_policy_device_state_summary"):
            summary = getattr(self.dm, name)

            self.assertNotIsInstance(summary, EntityCollection, f"{name} is a singleton")
            self.assertIsInstance(summary.get().execute_query(), type(summary))

    @requires_delegated(*CONFIGURATION)
    def test_04_the_settings_catalog_carries_categories(self):
        """``configurationCategories`` exists on the preview root only and is service-provided."""
        categories = self.read(self.dm_beta.configuration_categories, "configurationCategories")
        category = self.row_or_skip(categories, "settings catalog category")

        self.assertIsNotNone(category.get_property("displayName"))

    @requires_delegated(*CONFIGURATION)
    def test_05_reusable_policy_settings_are_listed(self):
        """Reusable settings are what a Settings Catalog policy may refer to."""
        self.read(self.dm_beta.reusable_policy_settings, "reusablePolicySettings")


class TestTroubleshootingAndAudit(IntuneCase):
    """The two logs an administrator reads first."""

    @requires_delegated(*CONFIGURATION)
    def test_01_troubleshooting_events_are_listed(self):
        """Troubleshooting events are a preview-root collection."""
        self.read(self.dm_beta.troubleshooting_events, "troubleshootingEvents")

    @requires_delegated(*APPS)
    def test_02_the_tenant_audit_log_is_listed(self):
        """Intune's own audit log lives under ``deviceManagement``, not under ``auditLogs``."""
        events = self.read(self.dm.audit_events, "auditEvents")
        event = self.row_or_skip(events, "Intune audit event")

        self.assertIsNotNone(event.get_property("displayName"))
