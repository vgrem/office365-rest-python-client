from tests.decorators import requires_app_permission, requires_delegated
from tests.graph_case import GraphApplicationTestCase


class TestIdentity(GraphApplicationTestCase):
    @requires_app_permission("IdentityProvider.Read.All", "IdentityProvider.ReadWrite.All")
    def test1_list_identity_providers(self):
        """List identity providers"""
        result = self.client.identity.identity_providers.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("IdentityUserFlow.Read.All", or_roles=["Global Administrator"])
    def test2_list_user_flows(self):
        """List B2X user flows"""
        result = self.client.identity.b2x_user_flows.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("IdentityProvider.Read.All", or_roles=["Global Administrator"])
    def test3_available_provider_types(self):
        """List available identity provider types"""
        result = self.client.identity.identity_providers.available_provider_types().execute_query()
        self.assertIsNotNone(result.value)

    # @requires_directory_role(
    #    "Global Reader", "Security Operator", "Security Reader", "Security Administrator"
    # )
    @requires_app_permission("IdentityRiskyUser.Read.All")
    def test4_list_risky_users(self):
        """List risky users"""
        result = self.client.identity_protection.risky_users.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission(
        "Policy.ReadWrite.AuthenticationFlows",
        "EventListener.Read.All",
        "EventListener.ReadWrite.All",
        "Application.Read.All",
        "Application.ReadWrite.All",
    )
    def test5_list_authentication_event_listeners(self):
        """List authentication event listeners"""
        result = self.client.identity.authentication_event_listeners.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("Policy.Read.All", "Policy.ReadWrite.ConditionalAccess")
    def test6_list_conditional_access_policies(self):
        """List conditional access policies"""
        result = self.client.identity.conditional_access.policies.get().execute_query()
        self.assertIsNotNone(result.resource_path)
