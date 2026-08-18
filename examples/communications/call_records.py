"""
List Microsoft Teams call records — call quality and telephony reporting.

Requires application permission ``CallRecords.Read.All``.

https://learn.microsoft.com/en-us/graph/api/callrecords-callrecord-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List recent call records")
    parser.add_argument("--limit", type=int, default=20, help="Max call records")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    records = client.communications.call_records.top(args.limit).get().execute_query()
    print(f"Call records ({len(records)}):\n")
    for r in records:
        props = r.properties
        duration = None
        if r.start_date_time and r.end_date_time:
            duration = f"{(r.end_date_time - r.start_date_time).total_seconds():.0f}s"
        print(
            f"  {r.start_date_time or '?'}  type={props.get('type', '?')}  "
            f"duration={duration or '?'}  participants={len(r.participants)}"
        )


if __name__ == "__main__":
    main()
