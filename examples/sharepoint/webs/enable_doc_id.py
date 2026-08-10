"""Assigns a Document ID to a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url


def main():
    parser = argparse.ArgumentParser(description="Assign a Document ID prefix to the site")
    parser.add_argument("--prefix", default="DOCID", help="document ID prefix (default: DOCID)")
    args = parser.parse_args()

    ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
    ctx.web.assign_document_id(args.prefix).execute_query()
    print(f"Document IDs assigned with prefix '{args.prefix}'")


if __name__ == "__main__":
    main()
