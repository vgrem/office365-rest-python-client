"""
Add a tenant theme.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.portal.theme_manager import ThemeManager

ctx = ClientContext("https://contoso-admin.sharepoint.com").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

manager = ThemeManager(ctx)
theme = {
    "themePrimary": "#0078d4",
    "themeLighterAlt": "#eff6fc",
    "themeLighter": "#deecf9",
}
manager.add_tenant_theme("Contoso Theme", json.dumps(theme)).execute_query()
print("Theme added")
