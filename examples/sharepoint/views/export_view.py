"""
Export a view's column mapping (field internal name to title) as JSON.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Export a view's field mapping as JSON")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--view", required=True, help="View title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    list_object = ctx.web.lists.get_by_title(args.list_title)
    view_fields = list_object.views.get_by_title(args.view).view_fields.get().execute_query()

    fields = [list_object.fields.get_by_internal_name_or_title(field_name).get() for field_name in view_fields]
    ctx.execute_batch()  # prefer batch over sequential round trips

    fields_json = {f.internal_name: f.title for f in fields}
    print(json.dumps(fields_json))


if __name__ == "__main__":
    main()
