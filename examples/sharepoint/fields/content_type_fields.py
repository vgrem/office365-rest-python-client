"""
Add a site column to a content type and list its field links.

Content types define which columns appear on items; field links control
column membership and display order.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Add a field to a content type")
    parser.add_argument("--content-type", default="Item", help="Content type name")
    parser.add_argument("--field", required=True, help="Field internal name or title")
    parser.add_argument("--list-title", help="List to scope the content type to (default: web)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    if args.list_title:
        content_type = ctx.web.lists.get_by_title(args.list_title).content_types.get_by_name(args.content_type)
    else:
        content_type = ctx.web.content_types.get_by_name(args.content_type)
    field = ctx.web.fields.get_by_internal_name_or_title(args.field)

    content_type.field_links.add(field).execute_query()
    print(f"Added '{args.field}' to content type '{args.content_type}'\n")

    links = content_type.field_links.get().execute_query()
    print(f"Field links ({len(links)}):")
    for link in links:
        print(f"  {link.properties.get('FieldInternalName')}")


if __name__ == "__main__":
    main()
