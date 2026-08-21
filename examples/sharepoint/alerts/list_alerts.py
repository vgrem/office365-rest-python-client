"""
List alerts for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="List alerts for the current user").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    alerts = ctx.web.current_user.alerts.get().execute_query()
    print(f"Alerts for the current user ({len(alerts)}):")
    for a in alerts:
        title = a.properties.get("Title", "?")
        alert_type = a.properties.get("AlertType", "?")
        frequency = a.alert_frequency
        print(f"  {title}  (type: {alert_type}, frequency: {frequency})")


if __name__ == "__main__":
    main()
