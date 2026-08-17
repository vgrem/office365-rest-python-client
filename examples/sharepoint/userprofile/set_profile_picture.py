"""
Set the current user's profile picture.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Set the current user's profile picture")
    parser.add_argument("--path", required=True, help="Path to the image file (e.g. .jpg, .png)")
    args = parser.parse_args()

    try:
        with open(args.path, "rb") as f:
            picture = f.read()
    except OSError as e:
        sys.exit(f"Failed to read {args.path}: {e}")

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ctx.people_manager.set_my_profile_picture(picture).execute_query()
    print(f"Profile picture set from {args.path}")


if __name__ == "__main__":
    main()
