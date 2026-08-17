"""
Create a content type that inherits from a parent content type.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a content type from a parent")
    parser.add_argument("--name", required=True, help="Content type name")
    parser.add_argument("--description", default="", help="Content type description")
    parser.add_argument("--parent", default="Document", help="Parent content type name")
    parser.add_argument("--keep", action="store_true", help="Keep the content type (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    parent_ct = ctx.web.content_types.get_by_name(args.parent)
    ct = ctx.web.content_types.create(
        name=args.name,
        description=args.description,
        parent_content_type=parent_ct,
    ).execute_query()
    print(f"Content type created: {ct.name}  (id: {ct.string_id}, parent: {parent_ct.name})")

    if not args.keep:
        ct.delete_object().execute_query()
        print("  (removed after demo)")


if __name__ == "__main__":
    main()
