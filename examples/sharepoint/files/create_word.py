"""
Demonstrates how to create a Word document in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    argparse.ArgumentParser(description="Create a Word document in the default document library").parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    result = ctx.web.default_document_library().create_document_with_default_name("", "docx").execute_query()
    print(f"'{result.value}' file has been created")


if __name__ == "__main__":
    main()
