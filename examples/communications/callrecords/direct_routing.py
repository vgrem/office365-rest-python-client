"""
The Direct Routing log read as a quality report: what left through the SBC, and why the
failed calls failed.

``getDirectRoutingCalls`` returns a **flat log**, not entities: the rows are
``DirectRoutingLogRow`` values wrapped in a ``ClientResult``, so read ``.value`` before
iterating. Grouping those rows by the final SIP phrase is what answers the question a voice
team actually asks — whether calls are being lost at the INVITE or at the RINGING — while a
list of a thousand rows answers nothing.

Requires the application permission ``CallRecords.Read.All``.

https://learn.microsoft.com/en-us/graph/api/callrecords-callrecord-getdirectroutingcalls
"""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

NO_RESPONSE = "no SIP response"


def main():
    parser = argparse.ArgumentParser(description="Direct Routing call quality over a window")
    parser.add_argument("--days", type=int, default=7, help="how far back to look")
    parser.add_argument("--top", type=int, default=5, help="how many SIP phrases to rank")
    parser.add_argument("--samples", type=int, default=5, help="how many failed calls to show")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    to_datetime = datetime.now(timezone.utc)
    rows = (
        client.communications.call_records.get_direct_routing_calls(
            from_datetime=to_datetime - timedelta(days=args.days),
            to_datetime=to_datetime,
        )
        .execute_query()
        .value
    )

    failed = [row for row in rows if not row.successfulCall]
    print(f"{len(rows)} call(s) in {args.days} day(s): {len(rows) - len(failed)} answered, {len(failed)} failed")

    if failed:
        print(f"\nWhere the {len(failed)} failed calls ended:")
        for phrase, count in Counter(row.finalSipCodePhrase or NO_RESPONSE for row in failed).most_common(args.top):
            print(f"  {count:>5}  {phrase}")

        print(f"\nThe first {min(args.samples, len(failed))}:")
        for row in failed[: args.samples]:
            started = f"{row.startDateTime:%Y-%m-%d %H:%M}" if row.startDateTime else "     ?        "
            print(f"  {started}  {row.callerNumber} -> {row.calleeNumber}  {row.finalSipCodePhrase or NO_RESPONSE}")


if __name__ == "__main__":
    main()
