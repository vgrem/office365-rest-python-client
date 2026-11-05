"""
Your own presence: read it, hold an override for a shift, and put a message beside it.

``get`` answers what colleagues see. ``set`` writes a *preferred* presence — Teams shows it
over what you are actually doing — and ``clear`` takes it down again, so a shift that ends
early does not leave you "Available" for the rest of the day. ``message`` is the one-line
note a colleague reads instead of guessing.

Only your own presence can be changed with delegated credentials: Graph refuses another
user's ("Cannot set the presence of another user"), which needs an application permission.

Requires the delegated permissions ``Presence.Read`` and, to write, ``Presence.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/presence-setuserpreferredpresence
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

AVAILABILITIES = ("Available", "Away", "BeRightBack", "Busy", "DoNotDisturb", "Offline")

#: Graph accepts a preferred presence for 5 minutes to 4 hours, and rejects anything else.
MIN_MINUTES, MAX_MINUTES = 5, 240


def main() -> None:
    parser = argparse.ArgumentParser(description="Read or set your own presence")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("get", help="what colleagues see now")
    setter = commands.add_parser("set", help="hold a preferred presence for a while")
    setter.add_argument("--availability", default="Available", choices=AVAILABILITIES)
    setter.add_argument("--activity", default="Available")
    setter.add_argument("--minutes", type=int, default=MAX_MINUTES, help="how long it holds")
    note = commands.add_parser("message", help="put a one-line note beside the availability")
    note.add_argument("text")
    note.add_argument("--minutes", type=int, help="when the note expires (default: never)")
    commands.add_parser("clear", help="drop the preferred presence")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    presence = client.me.presence

    if args.command == "get":
        current = presence.get().execute_query()
        print(f"{current.availability} / {current.activity}")
    elif args.command == "set":
        if not MIN_MINUTES <= args.minutes <= MAX_MINUTES:
            parser.error(f"--minutes must be {MIN_MINUTES}..{MAX_MINUTES}: Graph rejects the rest")
        presence.set_user_preferred_presence(args.availability, args.activity, f"PT{args.minutes}M").execute_query()
        print(f"Preferred presence: {args.availability} / {args.activity}, for {args.minutes} minutes")
    elif args.command == "message":
        expiry = datetime.now(timezone.utc) + timedelta(minutes=args.minutes) if args.minutes else None
        presence.set_status_message(args.text, expiry).execute_query()
        print(f"Status message: {args.text}" + (f" (until {expiry:%H:%M}Z)" if expiry else ""))
    else:
        presence.clear_user_preferred_presence().execute_query()
        print("Preferred presence cleared")


if __name__ == "__main__":
    main()
