"""
Field inventory: site columns (web scope) and list columns.

Surfaces the type, required, and hidden state admins need when planning
schema changes or migrations.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

LIST_TITLE = "Documents"


def print_fields(fields, scope: str) -> None:
    print(f"{scope} ({len(fields)}):")
    for f in fields:
        flags = " ".join(
            ["required" if f.properties.get("Required", False) else "", "hidden" if f.hidden else ""]
        ).strip()
        print(f"  {f.internal_name or '?':35s} {f.type_display_name or '?':18s} {flags}")


ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
print_fields(ctx.web.fields.get().execute_query(), "Site columns (web scope)")
target_list = ctx.web.lists.get_by_title(LIST_TITLE)
print_fields(target_list.fields.get().execute_query(), f"List columns ({LIST_TITLE})")
