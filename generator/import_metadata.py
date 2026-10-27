from argparse import ArgumentParser
from xml.dom import minidom

from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, password, site_url, tenant, username


def export_to_file(path: str, content: bytes) -> None:
    metadata_xml = minidom.parseString(content.decode("utf-8")).toprettyxml(indent="   ")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(metadata_xml)


parser = ArgumentParser()
parser.add_argument(
    "-e",
    "--endpoint",
    dest="endpoint",
    help="Import metadata endpoint",
    default="graph",
)
parser.add_argument(
    "-p",
    "--path",
    dest="path",
    default=None,
    help="Output file (default: ./metadata/Graph.xml, or ./metadata/GraphBeta.xml for the beta endpoint)",
)
parser.add_argument(
    "-V",
    "--version",
    dest="version",
    choices=[v.value for v in GraphVersion],
    default=GraphVersion.default().value,
    help="Microsoft Graph API version to download the metadata from (graph endpoint only)",
)

args = parser.parse_args()
if args.path is None:
    beta = args.endpoint == "graph" and GraphVersion(args.version).is_beta
    args.path = "./metadata/GraphBeta.xml" if beta else "./metadata/Graph.xml"

if args.endpoint == "sharepoint":
    print("Importing SharePoint model metadata...")
    ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
    result = ctx.get_metadata().execute_query()
    export_to_file(args.path, result.value)
elif args.endpoint == "graph":
    print(f"Importing Microsoft Graph model metadata ({args.version})...")
    client = GraphClient(tenant=tenant, version=GraphVersion(args.version)).with_client_secret(client_id, client_secret)
    result = client.get_metadata().execute_query()
    export_to_file(args.path, result.value)
