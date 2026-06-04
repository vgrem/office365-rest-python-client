"""Tests for Microsoft Graph People API."""

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPeople(GraphDelegatedTestCase):
    """Tests for the People API (relevant contacts and users)."""

    @requires_delegated(
        "People.Read",
        "People.Read.All",
        "User.Read",
        bypass_roles=["Global Administrator"],
    )
    def test1_list_relevant_people(self):
        """List people relevant to the signed-in user."""
        people = self.client.me.people.top(10).get().execute_query()
        self.assertIsNotNone(people.resource_path)
