"""
List alerts for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
alerts = ctx.web.current_user.alerts.get().execute_query()
for a in alerts:
    print(f"  {a.title}  (ID: {a.id}, type: {a.alert_type})")
