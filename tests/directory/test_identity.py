from unittest import TestCase

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant
from tests.decorators import requires_app_permission


class TestIdentity(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    @requires_app_permission("IdentityProvider.Read.All", "IdentityProvider.ReadWrite.All")
    def test1_list_identity_providers(self):
        result = self.client.identity.identity_providers.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test2_list_user_flows(self):
        result = self.client.identity.b2x_user_flows.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_available_provider_types(self):
        result = self.client.identity.identity_providers.available_provider_types().execute_query()
        self.assertIsNotNone(result.value)

    # @requires_directory_role(
    #    "Global Reader", "Security Operator", "Security Reader", "Security Administrator"
    # )
    @requires_app_permission("IdentityRiskyUser.Read.All")
    def test4_list_risky_users(self):
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
        result = self.client.identity.authentication_event_listeners.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("Policy.Read.All", "Policy.ReadWrite.ConditionalAccess")
    def test6_list_conditional_access_policies(self):
        result = self.client.identity.conditional_access.policies.get().execute_query()
        self.assertIsNotNone(result.resource_path)
