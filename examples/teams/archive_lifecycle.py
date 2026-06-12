"""
Find inactive teams and report archiving candidates.

Archived teams are read-only. Requires application permissions
Team.ReadBasic.All, TeamMember.Read.All, Directory.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

INACTIVITY_DAYS = 180


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    cutoff = datetime.now(timezone.utc) - timedelta(days=INACTIVITY_DAYS)

    teams = client.teams.get_all().execute_query()
    print(f"Found {len(teams)} teams\n")

    for team in teams:
        if team.is_archived:
            continue

        last_msg = None
        for channel in team.channels.get().execute_query():
            try:
                msgs = channel.messages.top(1).order_by("createdDateTime desc").get().execute_query()
                if msgs:
                    msg_date = msgs[0].created_date_time
                    if msg_date and (last_msg is None or msg_date > last_msg):
                        last_msg = msg_date
            except Exception:
                pass

        if last_msg is None or last_msg < cutoff:
            days = (datetime.now(timezone.utc) - last_msg).days if last_msg else float("inf")
            status = f"{days:.0f}d" if last_msg else "no messages"
            print(f"  {team.display_name}  ({team.visibility})  inactive: {status}")


if __name__ == "__main__":
    main()
