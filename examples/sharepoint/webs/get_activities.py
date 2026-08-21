"""
Gets web activities.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Get web activities")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    client = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)
    activities = client.web.activities.get().execute_query()
    for activity in activities:
        print(activity.action.facet_type)


if __name__ == "__main__":
    main()
