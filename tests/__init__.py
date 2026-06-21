import random
import string

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential

from tests.settings import (
    admin_site_url as test_admin_site_url,
)
from tests.settings import (
    admin_username as test_admin_principal_name,
)
from tests.settings import (
    cert_path as test_cert_path,
)
from tests.settings import (
    cert_thumbprint as test_cert_thumbprint,
)
from tests.settings import (
    client_id as test_client_id,
)
from tests.settings import (
    client_secret as test_client_secret,
)
from tests.settings import (
    password as test_password,
)
from tests.settings import (
    root_site_url as test_root_site_url,
)
from tests.settings import (
    site_url as test_site_url,
)
from tests.settings import (
    team_site_url as test_team_site_url,
)
from tests.settings import (
    tenant as test_tenant,
)
from tests.settings import (
    tenant_prefix as test_tenant_name,
)
from tests.settings import (
    user_principal as test_user_principal_name,
)
from tests.settings import (
    user_principal_alt as test_user_principal_name_alt,
)
from tests.settings import (
    username as test_username,
)

__all__ = [
    "test_admin_credentials",
    "test_admin_principal_name",
    "test_admin_site_url",
    "test_cert_thumbprint",
    "test_cert_path",
    "test_client_credentials",
    "test_client_id",
    "test_client_secret",
    "test_password",
    "test_root_site_url",
    "test_site_url",
    "test_team_site_url",
    "test_tenant",
    "test_tenant_name",
    "test_user_credentials",
    "test_user_principal_name",
    "test_user_principal_name_alt",
    "test_username",
    "create_unique_name",
    "create_unique_file_name",
]

test_client_credentials = ClientCredential(test_client_id, test_client_secret)

test_user_credentials = UserCredential(test_username, test_password)
test_admin_credentials = UserCredential(test_username, test_password)


def create_unique_name(prefix: str) -> str:
    return prefix + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


def create_unique_file_name(prefix: str, ext: str) -> str:
    return ".".join([create_unique_name(prefix), ext])
