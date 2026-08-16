"""
Shares a web (site) with a user by adding them to the corresponding group.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.external_site_option import ExternalSharingSiteOption
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Share a site with a user")
    parser.add_argument("--user", default=username, help="User principal name to share the site with")
    parser.add_argument(
        "--access",
        choices=["view", "edit", "owner"],
        default="view",
        help="Access level to grant (default: view)",
    )
    args = parser.parse_args()

    options = {
        "view": ExternalSharingSiteOption.View,
        "edit": ExternalSharingSiteOption.Edit,
        "owner": ExternalSharingSiteOption.Owner,
    }

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    result = ctx.web.share(args.user, options[args.access]).execute_query()
    if result.error_message is not None:
        sys.exit(f"Web sharing failed: {result.error_message}")

    print(f"Web '{result.url}' has been shared with user '{args.user}' ({args.access})")


if __name__ == "__main__":
    main()
