"""
Demonstrates how to create an Excel file in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Create an Excel file in the default document library").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.web.default_document_library().create_document_with_default_name("", "xlsx").execute_query()
    print(f"'{result.value}' file has been created")


if __name__ == "__main__":
    main()
