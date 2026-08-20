"""
Shared channels: create, share with another team, and verify access.

Shared channels extend collaboration across teams — members of other
teams can be added directly without adding them as guests to the host
team.

Subcommands:
  create       Create a shared channel and share it with a guest team
  list         Show teams a channel is shared with and allowed members
  has-access   Check whether a user can access a shared channel

Requires delegated or application permissions:
    Channel.Create                Create channels
    ChannelMember.ReadWrite.All   Manage channel members
    Channel.ReadBasic.All         Read channels
    Team.ReadBasic.All            Resolve teams

https://learn.microsoft.com/en-us/graph/api/resources/channel?view=graph-rest-1.0#shared-channels
"""

import argparse
import sys
from typing import Optional

from office365.graph_client import GraphClient
from office365.teams.members.aad_user_conversation import AadUserConversationMember
from office365.teams.team import Team
from tests.settings import client_id, client_secret, tenant


def _client() -> GraphClient:
    return GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)


def _get_team(client: GraphClient, team_id: Optional[str], name_hint: Optional[str]) -> Team:
    """Resolve a team by id, or by substring match on its display name."""
    if team_id:
        return client.teams[team_id].get().execute_query()
    teams = client.teams.get_all().select(["id", "displayName"]).execute_query()
    for team in teams:
        if name_hint and name_hint.lower() in (team.display_name or "").lower():
            return team
    sys.exit(f"Team not found matching '{name_hint}'. Pass --host-id/--guest-id to select by id.")


def _get_channel(team: Team, channel_id: str):
    return team.channels[channel_id].get().execute_query()


def cmd_create(client: GraphClient, args: argparse.Namespace) -> None:
    host = _get_team(client, args.host_id, args.host_name)
    guest = _get_team(client, args.guest_id, args.guest_name)

    channel = host.channels.add(
        display_name=args.name,
        description=args.description,
        membership_type="shared",
    ).execute_query()
    print(f"✓ Shared channel created: {channel.display_name} ({channel.id})")
    assert channel.id is not None and guest.id is not None

    host.channels[channel.id].shared_with_teams.add(teamId=guest.id).execute_query()
    print(f"✓ Channel shared with: {guest.display_name}")

    if args.member:
        users = client.users.filter(f"mail eq '{args.member}'").get().execute_query()
        if not users:
            sys.exit(f"User not found: {args.member}")
        user = users[0]
        member = AadUserConversationMember(host.context)
        member.set_property("userId", user.id)
        member.roles.add("owner")
        host.channels[channel.id].members.add_child(member)
        client.execute_query()
        print(f"✓ {user.display_name} added as channel owner")

    result = host.channels[channel.id].does_user_have_access(tenant_id=host.tenant_id).execute_query()
    print(f"Host team access check: {result.value}")


def cmd_list(client: GraphClient, args: argparse.Namespace) -> None:
    team = _get_team(client, args.team_id, args.team_name)
    channel = _get_channel(team, args.channel_id)
    print(f"Channel: {channel.display_name}")

    shared = channel.shared_with_teams.get().execute_query()
    print(f"  Shared with teams ({len(shared)}):")
    for info in shared:
        print(f"    {info.id}  host={info.is_host_team or False}")
        allowed = info.allowed_members.get().execute_query()
        for member in allowed:
            print(f"      member: {member.display_name or '?'}  roles={list(member.roles) if member.roles else []}")


def cmd_has_access(client: GraphClient, args: argparse.Namespace) -> None:
    team = _get_team(client, args.team_id, args.team_name)
    channel = _get_channel(team, args.channel_id)
    users = client.users.filter(f"mail eq '{args.user}'").get().execute_query()
    if not users:
        sys.exit(f"User not found: {args.user}")
    result = channel.does_user_have_access(user_principal_name=args.user).execute_query()
    print(f"{args.user} has access to '{channel.display_name}': {result.value}")


def _add_channel_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--channel", dest="channel_id", required=True, help="channel id")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shared channel management")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="create a shared channel and share it with a guest team")
    p.add_argument("--host-id", default=None, help="host team id (alternative to --host-name)")
    p.add_argument("--host-name", default=None, help="host team name substring")
    p.add_argument("--guest-id", default=None, help="guest team id (alternative to --guest-name)")
    p.add_argument("--guest-name", default=None, help="guest team name substring")
    p.add_argument("--name", required=True, help="channel display name")
    p.add_argument("--description", default=None, help="channel description")
    p.add_argument("--member", default=None, help="email of a user to add as channel owner")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("list", help="show teams a channel is shared with")
    p.add_argument("--team-id", default=None, help="host team id (alternative to --team-name)")
    p.add_argument("--team-name", default=None, help="host team name substring")
    _add_channel_arg(p)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("has-access", help="check whether a user can access a shared channel")
    p.add_argument("--team-id", default=None, help="host team id (alternative to --team-name)")
    p.add_argument("--team-name", default=None, help="host team name substring")
    _add_channel_arg(p)
    p.add_argument("--user", required=True, help="user email or UPN")
    p.set_defaults(func=cmd_has_access)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(_client(), args)


if __name__ == "__main__":
    main()
