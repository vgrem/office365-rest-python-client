"""
Update a field: title, required, hidden, group, description, form visibility, and indexing.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Update a field definition")
    parser.add_argument("--list-title", default="Documents", help="List containing the field")
    parser.add_argument("field", help="Field internal name or title")
    parser.add_argument("--title", help="New display name")
    parser.add_argument("--required", action="store_true", help="Mark the field as required")
    parser.add_argument("--hidden", action="store_true", help="Hide the field")
    parser.add_argument("--group", help="Field group")
    parser.add_argument("--description", help="Field description")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    field = ctx.web.lists.get_by_title(args.list_title).fields.get_by_internal_name_or_title(args.field)

    if args.title:
        field.set_property("Title", args.title)
    if args.required:
        field.set_property("Required", True)
    if args.hidden:
        field.set_property("Hidden", True)
    if args.group:
        field.set_property("Group", args.group)
    if args.description:
        field.set_property("Description", args.description)
    field.update().execute_query()

    # Form visibility (show in display form, hide from new/edit forms)
    field.set_show_in_new_form(False)
    field.set_show_in_edit_form(False)
    field.set_show_in_display_form(True)
    field.update().execute_query()

    # Enable the list index
    result = field.enable_index().execute_query()
    print(f"Field updated: {field.internal_name}  (indexed: {result.value})")


if __name__ == "__main__":
    main()
