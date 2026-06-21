"""
Report: scan all lists and libraries in a site and report their
compliance tag status.

Shows which lists have tags applied, which don't, and the tag
details (block delete, block edit, auto delete).

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

all_tags_result = ctx.site.get_available_tags().execute_query()
print(f"Available compliance tags: {len(all_tags_result.value)}\n")

tagged = 0
untagged = 0
for lst in ctx.web.lists.get().execute_query():
    if lst.hidden or lst.is_system_list:
        continue
    try:
        tag_info = lst.get_compliance_tag().execute_query()
        if tag_info and tag_info.value:
            t = tag_info.value
            print(f"  [{t.TagName or t.DisplayName}]  {lst.title}")
            tagged += 1
        else:
            untagged += 1
    except Exception:
        untagged += 1

print(f"\nTagged: {tagged}  Untagged: {untagged}")
