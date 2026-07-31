"""Demonstrates how to create a list in a SharePoint site

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from random import randint

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
list_name = "Tasks" + str(randint(0, 10000))
create_info = ListCreationInformation(list_name, None, ListTemplateType.Tasks)
lst = ctx.web.lists.add(create_info).execute_query()
print(f"List has been created: {lst.title}")
