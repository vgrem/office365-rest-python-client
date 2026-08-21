"""
Retrieves file check out status

https://support.microsoft.com/en-us/office/check-out-or-check-in-files-in-a-document-library-acce24cd-ab39-4fcf-9c4d-1ce3050dc602
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve file check out status")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file = ctx.web.get_file_by_server_relative_url(args.file_url).get().execute_query()

    if file.check_out_type == 0:
        print("The file is checked out for editing on the server")
    elif file.check_out_type == 1:
        print("The file is checked out for editing on the local computer.")
    else:
        print("The file is not checked out.")


if __name__ == "__main__":
    main()
