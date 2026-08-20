"""
Call records — Teams call quality analytics across the tenant.

Requires application permission CallRecords.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _endpoint_user(endpoint) -> str:
    """Best-effort UPN for a call endpoint (user endpoints only)."""
    if endpoint is None:
        return "?"
    try:
        user = endpoint.get_property("user")
    except AttributeError:
        return "?"
    return getattr(user, "user_principal_name", None) or str(user) or "?"


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    records = client.communications.call_records.get().execute_query()
    print(f"Call records: {len(records)}\n")

    for r in records:
        print(f"  {r.start_date_time}  {r.type_.name}  organizer={_endpoint_user(r.organizer)}")

    if records:
        print()
        recent = records[0]
        sessions = recent.sessions.get().execute_query()
        print(f"Sessions: {len(sessions)}")
        for s in sessions:
            caller = _endpoint_user(s.caller)
            callee = _endpoint_user(s.callee)
            modalities = [m.name for m in s.modalities]
            print(f"  {caller} -> {callee}  modalities={modalities}")

            for seg in s.segments.get().execute_query():
                print(f"    segment {seg.id}")


if __name__ == "__main__":
    main()
