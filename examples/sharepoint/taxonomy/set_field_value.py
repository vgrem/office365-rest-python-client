"""
Demonstrates how to set a taxonomy (managed metadata) field value on a list item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue
from office365.sharepoint.taxonomy.field_value_col import TaxonomyFieldValueCollection
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Set a taxonomy field value on a list item").parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    custom_list = ctx.web.lists.get_by_title("Requests")

    sweden = TaxonomyFieldValue("Sweden", "f9a6dae9-633c-474b-b35e-b235cf2b9e73")
    item = custom_list.add_item(
        {
            "Title": "New item",
            "Country": sweden,
            "Countries": TaxonomyFieldValueCollection(TaxonomyFieldValue, [sweden]),
        }
    ).execute_query()
    print(f"Item created: {item.id}")


if __name__ == "__main__":
    main()
