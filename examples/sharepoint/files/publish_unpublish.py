"""
Publish or unpublish a file for content approval.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Publish or unpublish a file for content approval")
    parser.add_argument("--file-url", default="Shared Documents/report.docx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file = ctx.web.get_file_by_server_relative_path(args.file_url)

    file.publish("Approved for team").execute_query()
    print("File published")

    # Later: unpublish
    # file.unpublish("Needs revision").execute_query()
    # print("File unpublished")


if __name__ == "__main__":
    main()
