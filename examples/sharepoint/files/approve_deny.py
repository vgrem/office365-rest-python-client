"""
Approve or deny a file submitted for content approval.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Approve or deny a file submitted for content approval")
    parser.add_argument("--file-url", default="Shared Documents/report.docx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file = ctx.web.get_file_by_server_relative_path(args.file_url)

    file.approve("Looks good").execute_query()
    print("File approved")

    # Or deny:
    # file.deny("Does not meet standards").execute_query()
    # print("File denied")


if __name__ == "__main__":
    main()
