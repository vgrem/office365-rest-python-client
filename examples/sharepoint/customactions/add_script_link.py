"""
Add a custom action that injects JavaScript (ScriptLink) on every page.

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Add a ScriptLink custom action")
    parser.add_argument("--title", default="Custom script", help="action title")
    parser.add_argument("--script", default="console.log('Loaded from custom action');", help="JavaScript to inject")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    action = ctx.web.user_custom_actions.add(
        title=args.title,
        location="ScriptLink",
        script_block=args.script,
    ).execute_query()
    print(f"Script link added: {action.properties.get('Id')}")


if __name__ == "__main__":
    main()
