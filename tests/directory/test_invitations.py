from tests.decorators import requires_app_permission
from tests.graph_case import GraphApplicationTestCase


class TestInvitations(GraphApplicationTestCase):
    @requires_app_permission("User.Invite.All", "Directory.ReadWrite.All", "User.ReadWrite.All")
    def test1_create_invitation(self):
        """Create an invitation for an external user"""
        invitation = self.client.invitations.create("admin@fabrikam.com", "https://myapp.contoso.com").execute_query()
        self.assertIsNotNone(invitation.resource_path)
