"""
Update a content type — change its description and group.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Update a content type")
    parser.add_argument("--name", required=True, help="Content type name")
    parser.add_argument("--description", required=True, help="New description")
    parser.add_argument("--group", help="New group")
    parser.add_argument("--keep", action="store_true", help="Keep the content type (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ct = ctx.web.content_types.get_or_add(name=args.name).execute_query()
    ct.set_property("Description", args.description)
    if args.group:
        ct.set_property("Group", args.group)
    ct.update().execute_query()
    print(f"Content type updated: {ct.name}  (description: {ct.description})")

    if not args.keep:
        ct.delete_object().execute_query()
        print("  (removed after demo)")


if __name__ == "__main__":
    main()
