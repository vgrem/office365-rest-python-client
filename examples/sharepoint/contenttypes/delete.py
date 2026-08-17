"""
Delete a content type from the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Delete a content type")
    parser.add_argument("--name", required=True, help="Content type name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ct = ctx.web.content_types.get_by_name(args.name).execute_query()
    ct.delete_object().execute_query()
    print(f"Content type deleted: {args.name}")


if __name__ == "__main__":
    main()
