"""
Generates a site script from an existing list.

Site scripts can be generated from existing lists to capture
their configuration for reuse.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Generate a site script from an existing list")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    target_list = ctx.web.default_document_library()
    result = target_list.get_site_script().execute_query()
    print(result.value)


if __name__ == "__main__":
    main()
