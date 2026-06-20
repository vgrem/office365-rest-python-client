"""
Contact management: create, read, update, and delete personal contacts.

Requires delegated permission Contacts.ReadWrite.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    folder = client.me.contact_folders.get_or_add("SDK Demo Contacts").execute_query()
    contact = folder.contacts.add(
        given_name="Maria",
        surname="Andersen",
        email_address="mariaa@contoso.onmicrosoft.com",
        business_phone="+1 555 123 4567",
    ).execute_query()
    print(f"Created: {contact.display_name}  {contact.primary_email_address}")

    contact.mobile_phone = "+1 555 987 6543"
    contact.job_title = "Senior Engineer"
    contact.update().execute_query()
    print("Updated: mobile & job title")

    contacts = folder.contacts.get().execute_query()
    print(f"\nContacts ({len(contacts)}):")
    for c in contacts:
        print(f"  {c.display_name}  {c.primary_email_address}")

    contact.delete_object().execute_query()
    print(f"Deleted: {contact.display_name}")


if __name__ == "__main__":
    main()
