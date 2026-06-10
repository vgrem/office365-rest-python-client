"""
Find inactive channels across all teams based on last message date.

Channels with no recent messages are candidates for archiving or
cleanup. Useful for reducing Teams noise and managing channel sprawl.

Inspired by Find-InactiveTeamsChannels.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Team.ReadBasic.All              List all teams
    Channel.ReadBasic.All           Read channels in each team
    ChannelMessage.Read.All         Read message timestamps
    ChannelSettings.ReadWrite.All   (optional) to archive inactive channels

https://learn.microsoft.com/en-us/graph/api/resources/channel
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

_DISPLAY_LIMIT = 30


def find_inactive_channels(days_threshold: int = 90) -> list[dict]:
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    inactive = []

    teams = client.teams.get_all().execute_query()
    for team in teams:
        channels = team.channels.get().execute_query()

        for channel in channels:
            last_message = None
            try:
                messages = team.channels[channel.id].messages.top(1).get().execute_query()
                if messages:
                    last_message = getattr(messages[0], "created_date_time", None)
            except Exception:
                pass

            if last_message and last_message < cutoff:
                days = (datetime.now(timezone.utc) - last_message).days
                inactive.append(
                    {
                        "team": team.display_name or "Unnamed",
                        "channel": channel.display_name or "Unnamed",
                        "channel_type": getattr(channel, "membership_type", "standard"),
                        "last_message": last_message,
                        "days_since": days,
                    }
                )
            elif not last_message:
                inactive.append(
                    {
                        "team": team.display_name or "Unnamed",
                        "channel": channel.display_name or "Unnamed",
                        "channel_type": getattr(channel, "membership_type", "standard"),
                        "last_message": None,
                        "days_since": days_threshold + 1,
                    }
                )

    inactive.sort(key=lambda x: x["days_since"], reverse=True)
    return inactive


def main():
    print("Finding inactive channels (no messages in 90+ days)...\n")
    channels = find_inactive_channels(days_threshold=90)

    if not channels:
        print("No inactive channels found.")
        return

    print(f"Found {len(channels)} inactive channels:\n")
    for c in channels[:_DISPLAY_LIMIT]:
        last = c["last_message"].strftime("%Y-%m-%d") if c["last_message"] else "Never"
        print(f"  Team: {c['team']}")
        print(f"  Channel: {c['channel']}  ({c['channel_type']})  last message: {last}")
        print()
    if len(channels) > _DISPLAY_LIMIT:
        print(f"... and {len(channels) - _DISPLAY_LIMIT} more")


if __name__ == "__main__":
    main()
