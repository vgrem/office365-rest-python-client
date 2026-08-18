"""
List the custom profile-card properties configured for the organization.

Requires delegated permission ``PeopleSettings.Read.All``.

https://learn.microsoft.com/en-us/graph/api/peopleadminsettings-list-profilecardproperties
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    props = client.admin.people.profile_card_properties.get().execute_query()
    print(f"Custom profile card properties ({len(props)}):")
    for p in props:
        data = p.properties
        labels = data.get("annotations", []) or []
        print(f"  {data.get('directoryPropertyName', '?'):35s}  labels: {len(labels)}")


if __name__ == "__main__":
    main()
