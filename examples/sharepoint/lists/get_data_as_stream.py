"""Demonstrates how to retrieve SharePoint list data as a stream using a CAML query

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

VIEW_XML = """
<View>
    <Query>
        <Where>
        </Where>
    </Query>
     <ViewFields>
        <FieldRef Name='Title' />
        <FieldRef Name='Created' />
        <FieldRef Name='Author' />
    </ViewFields>
    <RowLimit>100</RowLimit>
</View>
"""


def main():
    parser = argparse.ArgumentParser(description="Retrieve SharePoint list data as a stream")
    parser.add_argument("--server-relative-url", default="/Shared Documents", help="server-relative URL of the list")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(tenant, client_id, username, password)

    result = ctx.web.get_list_data_as_stream(args.server_relative_url, view_xml=VIEW_XML).execute_query()
    print(result.value)


if __name__ == "__main__":
    main()
