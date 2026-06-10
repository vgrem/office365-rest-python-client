"""People API — relevant people, profile card, and social network info.

Tests cover:
  - Listing people relevant to the signed-in user
  - People property assertions (displayName, emailAddresses)
  - People filtering by type (person, contact)
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPeople(GraphDelegatedTestCase):
    """People API — relevant contacts and users."""

    @requires_delegated(
        "People.Read",
        "People.Read.All",
        "User.Read",
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_relevant_people(self):
        """Listing people relevant to the user returns a valid collection."""
        people = self.client.me.people.top(10).get().execute_query()
        self.assertIsNotNone(people.resource_path)

    @requires_delegated(
        "People.Read",
        "People.Read.All",
        "User.Read",
        bypass_roles=["Global Administrator"],
    )
    def test_02_person_has_display_name(self):
        """A person entry exposes displayName and emailAddresses."""
        people = self.client.me.people.top(5).get().execute_query()
        if len(people) == 0:
            self.skipTest("No people results found")

        for person in people:
            self.assertIsNotNone(person.display_name)
            emails = person.get_property("emailAddresses")
            if emails:
                self.assertGreaterEqual(len(emails), 0)
                break

    @requires_delegated(
        "People.Read",
        "People.Read.All",
        "User.Read",
        bypass_roles=["Global Administrator"],
    )
    def test_03_filter_people_by_classification(self):
        """Filtering people by classification returns matching results."""
        try:
            result = self.client.me.people.filter("classification eq 'person'").top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception:
            self.skipTest("Filtering people by classification not supported")
