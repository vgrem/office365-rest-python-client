"""
Gets files within a folder.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Gets files within a folder")
    parser.add_argument("--folder-url", default="Shared Documents", help="folder url")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant=tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    root_folder = ctx.web.get_folder_by_server_relative_path(args.folder_url)
    ctx.load(root_folder, ["Files"])
    ctx.execute_query()
    for file in root_folder.files:
        print(file.name)


if __name__ == "__main__":
    main()
