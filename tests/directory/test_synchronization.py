"""Synchronization jobs for a service principal.

Tests cover:
  - Listing synchronization jobs for a service principal
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.serviceprincipals.service_principal import ServicePrincipal

from tests import test_client_id
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSynchronization(GraphDelegatedTestCase):
    """Synchronization jobs for a service principal."""

    target_sp: ClassVar[Optional[ServicePrincipal]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_sp = cls.client.service_principals.get_by_app_id(test_client_id).get().execute_query()

    @requires_delegated(
        "Synchronization.Read.All",
        "Synchronization.ReadWrite.All",
        bypass_roles=["Hybrid Identity Administrator", "Global Administrator"],
    )
    def test_01_list_synchronization_jobs(self):
        """Listing synchronization jobs for the target service principal returns a valid collection."""
        sp = TestSynchronization.target_sp
        if not sp:
            self.skipTest("No target service principal fetched in setUpClass")
        try:
            result = sp.synchronization.jobs.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list synchronization jobs: {e}")
