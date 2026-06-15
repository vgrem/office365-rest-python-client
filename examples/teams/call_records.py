"""
Call records — Teams call quality analytics across the tenant.

Requires application permission CallRecords.Read.All.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    records = client.communications.call_records.get().execute_query()
    print(f"Call records: {len(records)}\n")

    for r in records:
        print(f"  {r.start_date_time}  {r.type_.name}  organizer={r.organizer.user}")

    if records:
        print()
        recent = records[0]
        sessions = recent.sessions.get().execute_query()
        print(f"Sessions: {len(sessions)}")
        for s in sessions:
            caller = s.caller.user.user_principal_name if s.caller and s.caller.user else "?"
            callee = s.callee.user.user_principal_name if s.callee and s.callee.user else "?"
            modalities = [m.name for m in s.modalities]
            print(f"  {caller} -> {callee}  modalities={modalities}")

            segments = s.segments.get().execute_query()
            for seg in segments:
                print(f"    segment {seg.id}")


if __name__ == "__main__":
    main()
