"""
People search — find users via the SharePoint search API.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Search for people")
    parser.add_argument("--name", default="", help="Name filter, e.g. 'Smith'")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    query = "contentclass:SP.People" + (f" {args.name}" if args.name else "")
    result = ctx.search.query(
        query_text=query,
        select_properties=["AccountName", "PreferredName", "WorkEmail", "Department", "Title"],
        row_limit=20,
    ).execute_query()

    rows = result.value.PrimaryQueryResult.RelevantResults.Table.Rows
    print(f"People ({len(rows)}):")
    for row in rows:
        cells = row.Cells
        name = cells.get("PreferredName", "?")
        email = cells.get("WorkEmail", "?")
        print(f"  {name:30s}  {email:35s}  {cells.get('Department', '?')}")


if __name__ == "__main__":
    main()
