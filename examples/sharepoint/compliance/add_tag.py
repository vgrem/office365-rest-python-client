"""
Apply a compliance tag to a list or document library.

Requires ``Sites.ReadWrite.All`` to read and apply compliance tags.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

TAG_NAME = "Financial Records"

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

tags = ctx.site.get_available_tags().execute_query()
tag_id = next(
    (t.TagId for t in tags.value if TAG_NAME.lower() in (t.DisplayName or t.TagName or "").lower()),
    None,
)
if not tag_id:
    raise SystemExit(f"Tag '{TAG_NAME}' not found among available tags.")

target_list = ctx.web.lists.get_by_title("Documents")
target_list.set_compliance_tag(tag_id=tag_id).execute_query()
print(f"Compliance tag '{TAG_NAME}' applied to 'Documents' list.")
