from office365.outlook.contacts.contact import Contact

from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestOutlookContacts(GraphTestCase):
    target_contact: Contact = None

    @requires_delegated_permission("Contacts.ReadWrite")
    def test1_create_contact(self):
        result = self.client.me.contacts.add(
            "Pavel",
            "Bansky",
            "pavelb@a830edad9050849NDA1.onmicrosoft.com",
            "+1 732 555 0102",
        ).execute_query()
        self.assertEqual(result.email_addresses[0].name, "Pavel Bansky")
        self.__class__.target_contact = result

    @requires_delegated_permission("Contacts.Read", "Contacts.ReadWrite")
    def test2_list_contacts(self):
        result = self.client.me.contacts.get().execute_query()
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated_permission("Contacts.ReadWrite")
    def test3_update_contact(self):
        contact = self.__class__.target_contact
        self.assertIsNotNone(contact.id)
        contact.set_property("department", "Media").update().execute_query()

    @requires_delegated_permission("Contacts.ReadWrite")
    def test4_delete_contact(self):
        contact_id = self.__class__.target_contact.id
        self.__class__.target_contact.delete_object().execute_query()
        # verify
        contacts = self.client.me.contacts.get().execute_query()
        results = [c for c in contacts if c.id == contact_id]
        self.assertEqual(len(results), 0)
