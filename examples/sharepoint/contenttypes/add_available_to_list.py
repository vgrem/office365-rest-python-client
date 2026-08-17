"""
Add an existing site-level content type to a list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Add an existing site content type to a list")
    parser.add_argument("--ct-id", required=True, help="Content type id (e.g. 0x0120)")
    parser.add_argument("--list-title", default="Documents", help="Target list")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    target_list.content_types.add_available_content_type(args.ct_id).execute_query()
    print(f"Content type '{args.ct_id}' added to list: {target_list.title}")


if __name__ == "__main__":
    main()
