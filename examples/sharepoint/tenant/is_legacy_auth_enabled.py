"""
Checks whether legacy authentication protocols are enabled on the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from pprint import pprint

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import (
    admin_site_url,
    cert_path,
    cert_thumbprint,
    client_id,
    tenant,
)

tenant = Tenant.from_url(admin_site_url).with_client_certificate(
    tenant,
    client_id=client_id,
    thumbprint=cert_thumbprint,
    cert_path=cert_path,
)

details = tenant.get().execute_query()
pprint(details.legacy_auth_protocols_enabled)
