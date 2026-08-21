"""
Demonstrates how to create and delete a wiki page in the default document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.pages.template_file_type import TemplateFileType
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create and delete a wiki page in the default document library")
    parser.add_argument("--file-url", default="WikiPage 123.aspx", help="wiki page file name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    parent_folder = ctx.web.default_document_library().root_folder

    file = parent_folder.files.add_template_file(args.file_url, TemplateFileType.WikiPage).execute_query()

    file.delete_object().execute_query()


if __name__ == "__main__":
    main()
