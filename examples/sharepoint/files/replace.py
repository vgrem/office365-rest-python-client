"""
Demonstrates how to replace file content
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Replace file content")
    parser.add_argument("--path", default="../../data/report.csv", help="path to the local file")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    print("Uploading a new file...")
    with open(args.path, "rb") as f:
        target_file = ctx.web.default_document_library().root_folder.files.upload(f).execute_query()

    print("Replacing file content...")
    with open(args.path, "rb") as content_file:
        file_content = content_file.read()
    target_file.save_binary_stream(file_content).execute_query()

    print("Cleaning up resources...")
    target_file.delete_object().execute_query()


if __name__ == "__main__":
    main()
