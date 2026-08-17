"""Gets trending hash tags (up to 20 most popular over the past week).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
tags = ctx.people_manager.get_trending_tags(ctx).execute_query()
for tag in tags.items:
    print(f"  #{tag.name}  ({tag.count})")
