"""Gets the OneDrive (default document library) URL for a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Resolve a user's OneDrive URL")
    parser.add_argument("--user", default=None, help="account name (default: current user)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    if args.user:
        target = ctx.web.ensure_user(args.user).execute_query()
        assert target.login_name is not None
        result = ctx.people_manager.get_default_document_library(target).execute_query()
        print(f"OneDrive URL for {args.user}: {result.value}")
    else:
        me = ctx.web.current_user
        result = ctx.people_manager.get_default_document_library(me).execute_query()
        print(f"OneDrive URL: {result.value}")


if __name__ == "__main__":
    main()
