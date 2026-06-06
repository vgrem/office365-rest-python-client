"""Identity — providers, user flows, risky users, conditional access policies, and authentication event listeners.

Tests cover:
  - Listing identity providers
  - Listing B2X user flows
  - Listing available provider types
  - Listing risky users
  - Listing authentication event listeners
  - Listing conditional access policies
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestIdentity(GraphApplicationTestCase):
    """Identity providers, user flows, risky users, and conditional access."""

    @requires_application("IdentityProvider.Read.All", "IdentityProvider.ReadWrite.All")
    def test_01_list_identity_providers(self):
        """Listing identity providers returns a valid collection."""
        result = self.client.identity.identity_providers.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("IdentityUserFlow.Read.All")
    def test_02_list_user_flows(self):
        """Listing B2X user flows returns a valid collection."""
        result = self.client.identity.b2x_user_flows.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("IdentityProvider.Read.All")
    def test_03_available_provider_types(self):
        """Listing available identity provider types returns a value."""
        result = self.client.identity.identity_providers.available_provider_types().execute_query()
        self.assertIsNotNone(result.value)

    @requires_application("IdentityRiskyUser.Read.All")
    def test_04_list_risky_users(self):
        """Listing risky users returns a valid collection."""
        result = self.client.identity_protection.risky_users.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application(
        "Policy.ReadWrite.AuthenticationFlows",
        "EventListener.Read.All",
        "EventListener.ReadWrite.All",
        "Application.Read.All",
        "Application.ReadWrite.All",
    )
    def test_05_list_authentication_event_listeners(self):
        """Listing authentication event listeners returns a valid collection."""
        result = self.client.identity.authentication_event_listeners.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("Policy.Read.All", "Policy.ReadWrite.ConditionalAccess")
    def test_06_list_conditional_access_policies(self):
        """Listing conditional access policies returns a valid collection."""
        result = self.client.identity.conditional_access.policies.get().execute_query()
        self.assertIsNotNone(result.resource_path)
