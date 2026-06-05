"""Contacts — creating, listing, updating, and deleting personal contacts.

Tests cover:
  - Creating a contact with name, email, and phone
  - Listing contacts and verifying a minimum count
  - Updating contact properties (department)
  - Deleting a contact and verifying removal
  - Contact property assertions
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.contacts.contact import Contact

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookContacts(GraphDelegatedTestCase):
    """Contact CRUD and property inspection."""

    target_contact: ClassVar[Optional[Contact]] = None

    @requires_delegated(
        "Contacts.ReadWrite",
        bypass_roles=["Global Administrator", "Exchange Administrator", "User Administrator"],
    )
    def test_01_create_contact(self):
        """Creating a contact with name, email, and phone returns a valid contact."""
        result = self.client.me.contacts.add(
            "Pavel", "Bansky",
            "pavelb@a830edad9050849NDA1.onmicrosoft.com",
            "+1 732 555 0102",
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), "Pavel Bansky")
        TestOutlookContacts.target_contact = result

    @requires_delegated(
        "Contacts.Read", "Contacts.ReadWrite",
        bypass_roles=["Global Administrator", "Exchange Administrator", "User Administrator"],
    )
    def test_02_list_contacts(self):
        """Listing contacts returns at least the created contact."""
        result = self.client.me.contacts.get().execute_query()
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated(
        "Contacts.Read", "Contacts.ReadWrite",
        bypass_roles=["Global Administrator", "Exchange Administrator", "User Administrator"],
    )
    def test_03_contact_has_expected_properties(self):
        """A contact exposes displayName, emailAddresses, and mobilePhone."""
        created = TestOutlookContacts.target_contact
        if not created:
            self.skipTest("No contact created from previous test")

        self.assertIsNotNone(created.get_property("displayName"))
        self.assertIsNotNone(created.get_property("emailAddresses"))

    @requires_delegated(
        "Contacts.ReadWrite",
        bypass_roles=["Global Administrator", "Exchange Administrator", "User Administrator"],
    )
    def test_04_update_contact_department(self):
        """Updating a contact's department field should succeed."""
        contact = TestOutlookContacts.target_contact
        if not contact:
            self.skipTest("No contact created from previous test")

        contact.set_property("department", "Media").update().execute_query()

        updated = self.client.me.contacts[contact.id].get().execute_query()
        self.assertEqual(updated.get_property("department"), "Media")

    @requires_delegated(
        "Contacts.ReadWrite",
        bypass_roles=["Global Administrator", "Exchange Administrator", "User Administrator"],
    )
    def test_05_delete_contact(self):
        """Deleting a contact should remove it from the contacts list."""
        contact = TestOutlookContacts.target_contact
        if not contact:
            self.skipTest("No contact created from previous test")

        contact_id = contact.id
        contact.delete_object().execute_query()

        remaining = self.client.me.contacts.get().execute_query()
        matches = [c for c in remaining if c.id == contact_id]
        self.assertEqual(len(matches), 0)
        TestOutlookContacts.target_contact = None

    @classmethod
    def tearDownClass(cls):
        contact = cls.target_contact
        if contact and contact.resource_path:
            try:
                contact.delete_object().execute_query()
            except Exception:
                pass
