"""
Retrieves SharePoint sites using search query.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Retrieve SharePoint sites using search query").parse_args()

    client = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    result = client.search.query("contentclass:STS_Site").execute_query()
    results = result.value.PrimaryQueryResult.RelevantResults
    for row in results.Table.Rows:
        url = row.Cells["Path"]
        print(url)


if __name__ == "__main__":
    main()
