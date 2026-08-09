"""Demonstrates how to import list items in bulk into a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from faker import Faker
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from tests.settings import client_id, password, team_site_url, tenant, username


def load_source(amount=1000):
    fake = Faker()
    result = []
    for _ in range(amount):
        entry = {
            "Title": fake.name(),
            "FullName": fake.name(),
            "Email": fake.email(),
            "Company": fake.company(),
            "WorkPhone": fake.phone_number(),
            "WorkAddress": fake.street_address(),
            "WorkCity": fake.city(),
            "WorkZip": fake.postcode(),
            "WorkCountry": fake.country(),
            # "WebPage": {"Url": fake.url()},
        }
        result.append(entry)

    return result


def run_import(source_data: list, target_list: List) -> None:
    for contact in source_data:
        target_list.add_item(contact)

    items_result = {"added": 0}

    def _print_progress(return_types) -> None:
        items_result["added"] += len([t for t in return_types if isinstance(t, ListItem)])
        print(f"{items_result['added']} items added")

    ctx.execute_batch(20, success_callback=lambda r: _print_progress(r))


if __name__ == "__main__":
    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    contacts = load_source()
    contacts_list = ctx.web.lists.get_by_title("Contacts_Large").execute_query()
    run_import(contacts, contacts_list)
