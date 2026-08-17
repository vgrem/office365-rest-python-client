"""
Clear the compliance tag from a list or document library.

Requires ``Sites.FullControl.All`` to clear the compliance tag.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Clear the compliance tag from a list")
    parser.add_argument("--list-title", default="Documents", help="Target list or library")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    target_list.set_compliance_tag("").execute_query()
    print(f"Compliance tag cleared from '{args.list_title}' list.")


if __name__ == "__main__":
    main()
