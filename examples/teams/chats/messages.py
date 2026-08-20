"""
Chat messaging: send, reply, list, export, and an activity digest.

The digest subcommand shows the most recently active chats for a user,
sorted by last activity.

Requires delegated permission ``Chat.ReadWrite`` / ``Chat.Read`` or
application permission ``Chat.ReadWrite.All`` / ``Chat.Read.All``.

https://learn.microsoft.com/en-us/graph/api/chatmessage-list
https://learn.microsoft.com/en-us/graph/api/chatmessage-post
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.teams.chats.messages.message import ChatMessage
from tests.settings import client_id, client_secret, tenant


def _client() -> GraphClient:
    return GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)


def _resolve_user(client: GraphClient, user_ref: str) -> User:
    user = client.users[user_ref].get().execute_query()
    if user is None:
        sys.exit(f"User not found: {user_ref}")
    return user


def _fmt_time(dt) -> str:
    if isinstance(dt, datetime):
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    return str(dt or "?")


def _body_content(message: ChatMessage) -> str:
    return str(message.body.content or "") if message.body else ""


def _fmt_author(message: ChatMessage) -> str:
    from_ = message.properties.get("from", None)
    if from_ is None:
        return "?"
    user = from_.properties.get("user", None) if hasattr(from_, "properties") else None
    if user is None and isinstance(from_, dict):
        user = from_.get("user", None)
    if user is None:
        return "?"
    if hasattr(user, "properties"):
        return str(user.properties.get("displayName", "?") or "?")
    if isinstance(user, dict):
        return str(user.get("displayName", "?") or "?")
    return "?"


def cmd_send(client: GraphClient, args: argparse.Namespace) -> None:
    chat = client.chats[args.chat_id].get().execute_query()
    message = chat.messages.add(args.content).execute_query()
    print(f"✓ Message sent to chat {args.chat_id}: {message.id}")


def cmd_reply(client: GraphClient, args: argparse.Namespace) -> None:
    chat = client.chats[args.chat_id].get().execute_query()
    message = chat.messages[args.message_id]
    reply = message.replies.add(args.content).execute_query()
    print(f"✓ Reply added: {reply.id}")


def cmd_list(client: GraphClient, args: argparse.Namespace) -> None:
    chat = client.chats[args.chat_id].get().execute_query()
    messages = chat.messages.order_by("createdDateTime desc").top(args.top).get().execute_query()
    print(f"Recent messages in chat {args.chat_id} ({len(messages)}):")
    for message in messages:
        preview = _body_content(message).replace("\n", " ")[:70]
        print(f"  {_fmt_time(message.created_datetime)}  {_fmt_author(message):20s}  {preview}")


def cmd_export(client: GraphClient, args: argparse.Namespace) -> None:
    chat = client.chats[args.chat_id].get().execute_query()
    messages = chat.messages.get_all().execute_query()
    lines = []
    for message in messages:
        record = {
            "id": message.id,
            "created": _fmt_time(message.created_datetime),
            "author": _fmt_author(message),
            "body": _body_content(message),
        }
        if args.output:
            lines.append(json.dumps(record))
        else:
            print(f"{record['created']}  {record['author']:20s}  {record['body']}")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print(f"✓ Exported {len(lines)} messages to {args.output}")


def cmd_digest(client: GraphClient, args: argparse.Namespace) -> None:
    if args.me:
        user = client.me.get().execute_query()
    else:
        user = _resolve_user(client, args.user)
    if user is None:
        sys.exit("Could not resolve the user.")

    chats = user.chats.top(args.top).get().execute_query()
    rows = []
    for chat in chats:
        body = chat.last_message_preview.body
        preview = str(body.content or "") if body else ""
        rows.append(
            (
                chat.last_updated_datetime or chat.created_datetime,
                chat.chat_type or "?",
                chat.topic or "-",
                preview,
            )
        )
    rows.sort(key=lambda r: r[0], reverse=True)

    print(f"Chat activity digest for {user.display_name or user.id} ({len(rows)} chats):")
    for last, chat_type, topic, preview in rows:
        print(f"  {_fmt_time(last)}  {chat_type:8s} {topic:20s}  {preview}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chat messaging and activity")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("send", help="send a message to a chat")
    p.add_argument("--chat", dest="chat_id", required=True, help="chat id")
    p.add_argument("--content", required=True, help="message text")
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("reply", help="reply to a chat message")
    p.add_argument("--chat", dest="chat_id", required=True, help="chat id")
    p.add_argument("--message", dest="message_id", required=True, help="message id to reply to")
    p.add_argument("--content", required=True, help="reply text")
    p.set_defaults(func=cmd_reply)

    p = sub.add_parser("list", help="list recent messages in a chat")
    p.add_argument("--chat", dest="chat_id", required=True, help="chat id")
    p.add_argument("--top", type=int, default=10, help="number of messages (default 10)")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("export", help="export all messages in a chat")
    p.add_argument("--chat", dest="chat_id", required=True, help="chat id")
    p.add_argument("--output", default=None, help="optional JSONL output file (otherwise prints)")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("digest", help="recently active chats for a user")
    p.add_argument("--user", default=None, help="user id or UPN (app-only)")
    p.add_argument("--me", action="store_true", help="the signed-in user (delegated)")
    p.add_argument("--top", type=int, default=20, help="maximum number of chats (default 20)")
    p.set_defaults(func=cmd_digest)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(_client(), args)


if __name__ == "__main__":
    main()
