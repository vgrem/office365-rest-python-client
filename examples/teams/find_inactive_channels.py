"""
Find inactive channels across all teams based on last message date.

Requires delegated permissions: Team.ReadBasic.All, Channel.ReadBasic.All,
ChannelMessage.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    num_days = 90
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    cutoff = datetime.now(timezone.utc) - timedelta(days=num_days)

    inactive = []
    for team in client.teams.get().top(30).execute_query():
        for channel in team.channels.get().execute_query():
            last = None
            try:
                messages = channel.messages.top(1).order_by("createdDateTime desc").get().execute_query()
                if messages:
                    last = messages[0].created_datetime
            except Exception:
                pass
            if last is None or last < cutoff:
                inactive.append(
                    (
                        team.display_name,
                        channel.display_name,
                        last,
                    )
                )

    print(f"Inactive channels ({num_days}+ days): {len(inactive)}")
    for team, ch, last in sorted(inactive, key=lambda x: x[2] or datetime.min):
        print(f"  {team}  {ch}  {last.strftime('%Y-%m-%d') if last else 'Never'}")


if __name__ == "__main__":
    main()
