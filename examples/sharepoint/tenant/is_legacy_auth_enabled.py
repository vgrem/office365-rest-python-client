"""
This example enables legacy authentication protocols on the tenant
"""

from pprint import pprint

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_cert_path,
    test_cert_thumbprint,
    test_client_id,
    test_tenant,
)

tenant = Tenant.from_url(test_admin_site_url).with_client_certificate(
    test_tenant,
    client_id=test_client_id,
    thumbprint=test_cert_thumbprint,
    cert_path=test_cert_path,
)

details = tenant.get().execute_query()
pprint(details.legacy_auth_protocols_enabled)
