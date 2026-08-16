"""
Provision multiple typed fields on a list from a schema specification.

Maps a name -> FieldType schema (like migration tools do) and creates
each field via the generic FieldCreationInformation.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.creation_information import FieldCreationInformation
from office365.sharepoint.fields.type import FieldType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

LIST_TITLE = "Tasks"
FIELDS = {
    "CustomerName": FieldType.Text,
    "Quantity": FieldType.Number,
    "DueDate": FieldType.DateTime,
    "Status": FieldType.Choice,
    "Notes": FieldType.Note,
}


def main():
    parser = argparse.ArgumentParser(description="Provision typed fields from a schema spec")
    parser.add_argument("--list-title", default=LIST_TITLE, help="Target list")
    parser.add_argument("--keep", action="store_true", help="Keep created fields (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_fields = ctx.web.lists.get_by_title(args.list_title).fields

    created = []
    for name, field_type in FIELDS.items():
        info = FieldCreationInformation(Title=name, FieldTypeKind=field_type)
        if field_type == FieldType.Choice:
            info.Choices = ["Not Started", "In Progress", "Completed", "Deferred"]
        field = target_fields.add_field(info).execute_query()
        created.append(field)
        print(f"  created {name:16s} ({field_type.name}) -> {field.internal_name}")

    if not args.keep:
        for field in created:
            field.delete_object().execute_query()
        print("  (fields removed after demo)")


if __name__ == "__main__":
    main()
