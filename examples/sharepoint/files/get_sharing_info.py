"""
Enumerates files along with role assignments
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.type import PrincipalType
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
doc_lib = ctx.web.default_document_library()
# retrieve all the files from a library
items = (
    doc_lib.items.select(["FSObjType", "EncodedAbsUrl", "Id"])
    .filter("FSObjType eq 0")
    .get_all()
    .execute_query()
)

# per every list item (file facet) retrieve role assignments (where role assignment is associated with a principal,
# which could be a user or a group)
for item in items:
    role_assignments = item.role_assignments.expand(["Member"]).get().execute_query()
    print(f"File: {item.properties['EncodedAbsUrl']}")
    for ra in role_assignments:
        if ra.member.principal_type == PrincipalType.SharePointGroup:
            print(ra.member)
