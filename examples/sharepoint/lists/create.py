"""Demonstrates how to create a list in a SharePoint site

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a SharePoint list")
    parser.add_argument("title", help="Title of the list to create")
    parser.add_argument(
        "--type",
        default="GenericList",
        help="List template type name, e.g. GenericList, Tasks, DocumentLibrary (default: GenericList)",
    )
    args = parser.parse_args()

    template_type = ListTemplateType[args.type]
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    create_info = ListCreationInformation(args.title, None, template_type)
    lst = ctx.web.lists.add(create_info).execute_query()
    print(f"List has been created: {lst.title}")


if __name__ == "__main__":
    main()
