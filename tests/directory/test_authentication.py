from tests.decorators import requires_application, requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestAuthentication(GraphDelegatedTestCase):
    @requires_delegated("UserAuthenticationMethod.Read.All", bypass_roles=["Global Administrator"])
    def test1_list_methods(self):
        """List authentication methods for the current user"""
        result = self.client.me.authentication.methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("Policy.Read.All", "Policy.ReadWrite.ConditionalAccess")
    def test2_list_strength_policies(self):
        """List authentication strength policies"""
        result = self.client.policies.authentication_strength_policies.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application(
        "UserAuthenticationMethod.Read",
        "UserAuthenticationMethod.Read.All",
        "UserAuthenticationMethod.ReadWrite",
        "UserAuthenticationMethod.ReadWrite.All",
    )
    def test3_list_password_methods(self):
        """List password methods for the current user"""
        result = self.client.me.authentication.password_methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)
