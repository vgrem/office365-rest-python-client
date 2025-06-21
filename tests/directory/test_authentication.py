from tests.decorators import requires_app_permission
from tests.graph_case import GraphTestCase


class TestAuthentication(GraphTestCase):
    def test1_list_methods(self):
        result = self.client.me.authentication.methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("Policy.Read.All", "Policy.ReadWrite.ConditionalAccess")
    def test2_list_strength_policies(self):
        result = (
            self.client.policies.authentication_strength_policies.get().execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission(
        "UserAuthenticationMethod.Read",
        "UserAuthenticationMethod.Read.All",
        "UserAuthenticationMethod.ReadWrite",
        "UserAuthenticationMethod.ReadWrite.All",
    )
    def test3_list_password_methods(self):
        result = self.client.me.authentication.password_methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)
