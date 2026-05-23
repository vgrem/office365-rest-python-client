"""Demonstrates how to copy a field from one site to another using its schema XML

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/field
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_team_site_url, test_tenant, test_username

field_name = "DocScope"

source_ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
source_field = source_ctx.web.default_document_library().fields.get_by_internal_name_or_title(field_name)
source_ctx.load(source_field, ["SchemaXml"]).execute_query()
assert source_field.schema_xml is not None

target_ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = target_ctx.web.default_document_library()
target_field = target_list.fields.create_field_as_xml(source_field.schema_xml).execute_query()
target_field.delete_object().execute_query()
