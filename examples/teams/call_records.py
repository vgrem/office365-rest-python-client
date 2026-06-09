"""
Call records — Teams call quality analytics across the tenant.

Rich data model: call → sessions → segments → endpoints.
Useful for:
  - Identifying poor-quality calls (jitter, packet loss, latency)
  - Auditing direct routing call failures
  - Reporting on call modalities (audio, video, screen share)

Requires application permission ``CallRecords.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/callrecords-api-overview
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: list recent call records --
    records = client.communications.call_records.top(20).get().execute_query()
    print(f"Call records: {len(records)}\n")

    if not records:
        print("(No call records — may need CallRecords.Read.All permission or recent calls)")
        return

    for r in records:
        r_id = r.id or "?"
        call_type = r.properties.get("type", "?")
        modality = r.properties.get("modalities", [])
        start = r.start_date_time
        if hasattr(start, "strftime"):
            start = start.strftime("%Y-%m-%d %H:%M")
        end = r.end_date_time
        if hasattr(end, "strftime"):
            end = end.strftime("%Y-%m-%d %H:%M")

        user_count = r.properties.get("participants_count", "?")
        organizer = r.properties.get("organizer", {})
        org_upn = "?"
        if isinstance(organizer, dict):
            u = organizer.get("user", {})
            org_upn = u.get("userPrincipalName", "?") if isinstance(u, dict) else "?"

        failure = r.properties.get("failureInfo", {})
        failure_phase = failure.get("stage", "") if isinstance(failure, dict) else ""

        print(f"  {r_id[:20]:20s}  type={call_type:15s}  modality={str(modality[:3]):10s}  "
              f"users={user_count}  organizer={org_upn[:25]:25s}")
        print(f"    start={start}  end={end}  failure={failure_phase or 'none'}")

    # -- Step 2: drill into sessions for the most recent call --
    if records:
        print()
        recent = records[0]
        print(f"Drilling into call {recent.id[:20]}...")

        sessions = recent.sessions.get().execute_query()
        print(f"  Sessions: {len(sessions)}")

        for s in sessions:
            s_id = s.id[:15] if s.id else "?"
            callee = s.properties.get("callee", {}).get("user", {}).get("userPrincipalName", "?")
            caller = s.properties.get("caller", {}).get("user", {}).get("userPrincipalName", "?")
            modality = s.properties.get("modalities", [])
            print(f"    session {s_id}  caller={str(caller)[:25]:25s}  "
                  f"callee={str(callee)[:25]:25s}  modality={str(modality[:3]):10s}")

            # Segments within this session
            segments = s.segments.get().execute_query()
            for seg in segments:
                seg_id = seg.properties.get("id", "?")[:10]
                print(f"      segment {seg_id}")

                # Endpoint quality data
                endpoints = seg.properties.get("endpoints", [])
                for ep in endpoints:
                    name = ep.get("name", "?")
                    ep_type = ep.get("@odata.type", "?")
                    print(f"        endpoint={name}  type={str(ep_type).split('.')[-1][:20]}")


if __name__ == "__main__":
    main()
