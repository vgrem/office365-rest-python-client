from unittest import TestCase

from office365.graph_client import GraphClient

from tests import test_client_id, test_client_secret, test_tenant
from tests.decorators import requires_app_permission
from tests.graph_case import GraphSecretTestCase


class TestInvitations(GraphSecretTestCase):
    @requires_app_permission("User.Invite.All", "Directory.ReadWrite.All", "User.ReadWrite.All")
    def test1_create_invitation(self):
        invitation = self.client.invitations.create("admin@fabrikam.com", "https://myapp.contoso.com").execute_query()
        self.assertIsNotNone(invitation.resource_path)
