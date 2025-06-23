import os
import random
import string

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
from tests.config import SecEnvInterpolation, load_config


def create_unique_name(prefix: str) -> str:
    return prefix + "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )


def create_unique_file_name(prefix, ext):
    return ".".join([create_unique_name(prefix), ext])


settings = load_config()

# shortcuts
test_tenant_name = settings.get("default", "tenant_prefix")
test_tenant = settings.get("default", "tenant")

test_client_id = settings.get("client_credentials", "client_id")
test_client_secret = settings.get("client_credentials", "client_secret")


test_client_credentials = ClientCredential(
    settings.get("client_credentials", "client_id"),
    settings.get("client_credentials", "client_secret"),
)

test_user_credentials = UserCredential(
    settings.get("user_credentials", "username"),
    settings.get("user_credentials", "password"),
)

test_admin_credentials = UserCredential(
    settings.get("user_credentials", "username"),
    settings.get("user_credentials", "password"),
)

test_site_url = settings.get("default", "site_url")
test_root_site_url = settings.get("default", "root_site_url")
test_team_site_url = settings.get("default", "team_site_url")
test_admin_site_url = settings.get("default", "admin_site_url")

test_user_principal_name = settings.get("users", "test_user1")
test_user_principal_name_alt = settings.get("users", "test_user2")
test_admin_principal_name = settings.get("users", "test_user3")

test_cert_thumbprint = settings.get("certificate_credentials", "thumbprint")
test_cert_path = "{0}/selfsigncert.pem".format(os.path.dirname(__file__))

test_username = settings.get("user_credentials", "username")
test_password = settings.get("user_credentials", "password")
