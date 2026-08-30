"""
Demonstrates how to create a taxonomy field on a list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create taxonomy fields on a list")
    parser.add_argument("--list-title", default="Requests", help="list title")
    parser.add_argument("--term-set-id", default="3b712032-95c4-4bb5-952d-f85ae9288f99", help="term set id")
    parser.add_argument("--field-name", default="Country", help="single-value taxonomy field name")
    parser.add_argument("--multi-field-name", default="Countries", help="multi-value taxonomy field name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    custom_list = ctx.web.lists.ensure_list(args.list_title).get().execute_query()

    print("1. Adding a taxonomy field into list '{0}'...".format(custom_list.title))
    custom_list.fields.create_taxonomy_field(args.field_name, args.term_set_id).execute_query()

    print("2. Adding a taxonomy field into list '{0}'...".format(custom_list.title))
    custom_list.fields.create_taxonomy_field(
        args.multi_field_name, args.term_set_id, allow_multiple_values=True
    ).execute_query()


if __name__ == "__main__":
    main()
