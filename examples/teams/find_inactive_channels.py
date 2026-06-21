"""
Find inactive channels across all teams based on last message date.

Requires delegated permissions: Team.ReadBasic.All, Channel.ReadBasic.All,
ChannelMessage.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

NUM_DAYS = 90


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    cutoff = datetime.now(timezone.utc) - timedelta(days=NUM_DAYS)

    inactive = []
    for team in client.teams.get_all().execute_query():
        for channel in team.channels.get().execute_query():
            last = None
            try:
                messages = channel.messages.top(1).order_by("createdDateTime desc").get().execute_query()
                if messages:
                    last = messages[0].created_datetime
            except Exception:
                pass
            if last is None or last < cutoff:
                inactive.append((team.display_name, channel.display_name, last))

    print(f"Inactive channels ({NUM_DAYS}+ days): {len(inactive)}")
    for team, ch, last in inactive:
        print(f"  {team}  {ch}  {last.strftime('%Y-%m-%d') if last else 'Never'}")


if __name__ == "__main__":
    main()
