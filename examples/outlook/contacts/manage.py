"""
Contact management: create, read, update, and delete personal contacts.

Covers the full CRUD lifecycle for Outlook contacts, including
contact folders for organization.

Requires delegated permission ``Contacts.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/contact
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    # -- Step 1: create a contact folder --
    folder_name = "SDK Demo Contacts"
    folders = client.me.contact_folders.get().execute_query()
    folder = next((f for f in folders if f.display_name == folder_name), None)

    if folder is None:
        folder = client.me.contact_folders.add(folder_name).execute_query()
        print(f"Created contact folder: '{folder.display_name}' (id: {folder.id})")
    else:
        print(f"Using existing folder: '{folder.display_name}'")

    # -- Step 2: create a contact --
    contact = (
        folder.contacts.add(
            given_name="Maria",
            surname="Andersen",
            email_address="mariaa@contoso.onmicrosoft.com",
            business_phone="+1 555 123 4567",
        )
        .execute_query()
    )
    print(f"Created contact: {contact.display_name}  ({contact.primary_email_address.address})")

    # -- Step 3: update fields --
    contact.set_property("mobilePhone", "+1 555 987 6543")
    contact.set_property("jobTitle", "Senior Engineer")
    contact.update().execute_query()
    print(f"Updated contact: mobile & job title set.")

    # -- Step 4: add a second email address --
    # The email_addresses property is a collection — append to it
    contact.email_addresses.add("maria.andersen@personal.com")
    contact.update().execute_query()
    print(f"Added secondary email.")

    # -- Step 5: list all contacts in the folder --
    contacts = folder.contacts.get().execute_query()
    print(f"\nContacts in '{folder_name}' ({len(contacts)}):")
    for c in contacts:
        print(f"  {c.display_name:25s}  {c.primary_email_address.address or '':35s}  {c.mobile_phone or '':15s}")

    # -- Step 6: delete the contact --
    contact.delete_object().execute_query()
    print(f"\n✓ Deleted contact: {contact.display_name}")


if __name__ == "__main__":
    main()
