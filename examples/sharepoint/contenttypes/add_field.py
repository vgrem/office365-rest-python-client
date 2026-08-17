"""
Add an existing site column to a content type (as a field link).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Add a field to a content type")
    parser.add_argument("--name", required=True, help="Content type name")
    parser.add_argument("--field", required=True, help="Field internal name or title")
    parser.add_argument("--keep", action="store_true", help="Keep the content type (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ct = ctx.web.content_types.get_or_add(name=args.name).execute_query()
    field = ctx.web.fields.get_by_internal_name_or_title(args.field)
    ct.field_links.add(field).execute_query()
    print(f"Field added to content type: {field.internal_name}")

    if not args.keep:
        ct.delete_object().execute_query()
        print("  (content type removed after demo)")


if __name__ == "__main__":
    main()
