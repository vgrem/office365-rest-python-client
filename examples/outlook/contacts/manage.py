"""
Contact management: create, read, update, and delete personal contacts.

Requires delegated permission Contacts.ReadWrite.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    folders = client.me.contact_folders.get().execute_query()
    folder = next((f for f in folders if f.display_name == "SDK Demo Contacts"), None)
    if folder is None:
        folder = client.me.contact_folders.add("SDK Demo Contacts").execute_query()
        print(f"Created folder: {folder.display_name}")
    else:
        print(f"Using folder: {folder.display_name}")

    contact = folder.contacts.add(
        given_name="Maria",
        surname="Andersen",
        email_address="mariaa@contoso.onmicrosoft.com",
        business_phone="+1 555 123 4567",
    ).execute_query()
    print(f"Created: {contact.display_name}  {contact.primary_email_address.address}")

    contact.set_property("mobilePhone", "+1 555 987 6543")
    contact.set_property("jobTitle", "Senior Engineer")
    contact.update().execute_query()
    print("Updated: mobile & job title")

    contacts = folder.contacts.get().execute_query()
    print(f"\nContacts ({len(contacts)}):")
    for c in contacts:
        print(f"  {c.display_name}  {c.primary_email_address.address}")

    contact.delete_object().execute_query()
    print(f"Deleted: {contact.display_name}")


if __name__ == "__main__":
    main()
