"""
Create a taxonomy (managed metadata) site column bound to a term set.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a taxonomy field")
    parser.add_argument("--field", default="Country", help="Field display name")
    parser.add_argument("--term-set-id", required=True, help="Term set GUID")
    parser.add_argument("--allow-multiple", action="store_true", help="Allow multiple values")
    parser.add_argument("--keep", action="store_true", help="Keep the field (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    field = ctx.web.fields.create_taxonomy_field(
        args.field, args.term_set_id, allow_multiple_values=args.allow_multiple
    ).execute_query()
    print(f"Taxonomy field created: {field.internal_name}  (id: {field.id})")

    if not args.keep:
        field.delete_object().execute_query()
        print("  (field removed after demo)")


if __name__ == "__main__":
    main()
