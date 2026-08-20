"""
Chat inventory for a user.

Lists a user's chats with type, topic, member count, and last activity,
then summarizes the chat landscape (1:1 vs group vs meeting).

Use --me (delegated) for the signed-in user, or --user for app-only access.

Requires delegated permission ``Chat.Read`` or application permission
``Chat.Read.All``.

https://learn.microsoft.com/en-us/graph/api/chat-list
"""

import argparse
import sys
from collections import Counter
from datetime import datetime, timezone

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _client() -> GraphClient:
    return GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)


def _resolve_user(client: GraphClient, user_ref: str) -> User:
    user = client.users[user_ref].get().execute_query()
    if user is None:
        sys.exit(f"User not found: {user_ref}")
    return user


def _preview_body(message) -> str:
    body = message.properties.get("body", None)
    if body is None:
        return ""
    content = body.properties.get("content", "") if hasattr(body, "properties") else ""
    return str(content).replace("\n", " ")[:60]


def _fmt_time(dt) -> str:
    if isinstance(dt, datetime):
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    return str(dt or "?")


def main():
    parser = argparse.ArgumentParser(description="Chat inventory for a user")
    parser.add_argument("--user", default=None, help="user id or UPN (app-only)")
    parser.add_argument("--me", action="store_true", help="the signed-in user (delegated)")
    parser.add_argument("--top", type=int, default=50, help="maximum number of chats (default 50)")
    parser.add_argument("--skip-members", action="store_true", help="skip per-chat member lookups (faster)")
    args = parser.parse_args()

    client = _client()
    if args.me:
        user = client.me.get().execute_query()
    elif args.user:
        user = _resolve_user(client, args.user)
    else:
        sys.exit("Pass --me (delegated) or --user <id|UPN> (app-only).")
    if user is None:
        sys.exit("Could not resolve the user.")

    chats = user.chats.top(args.top).get().execute_query()
    print(f"Chats for {user.display_name or user.id} ({len(chats)}):")

    summary: Counter = Counter()
    total_members = 0
    for chat in chats:
        chat_type = chat.chat_type or "?"
        summary[chat_type] += 1
        preview = _preview_body(chat.last_message_preview)
        member_count = ""
        if not args.skip_members:
            members = chat.members.get().execute_query()
            member_count = f" members={len(members)}"
            total_members += len(members)
        topic = chat.topic or "-"
        print(
            f"  {chat.id:50s} {chat_type:8s} {topic:20s} last={_fmt_time(chat.last_updated_datetime)}"
            f"  {member_count}  {preview}"
        )

    print("\nSummary:")
    for chat_type, count in summary.most_common():
        print(f"  {chat_type:8s}: {count}")
    if not args.skip_members:
        print(f"  total members across chats: {total_members}")


if __name__ == "__main__":
    main()
