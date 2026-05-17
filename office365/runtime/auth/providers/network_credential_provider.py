from office365.runtime.auth.authentication_provider import AuthenticationProvider
from office365.runtime.http.request_options import RequestOptions


class NetworkCredentialProvider(AuthenticationProvider):
    """Provides credentials for password-based authentication schemes such as basic authentication"""

    def __init__(self, username, password):
        super().__init__()
        self.userCredentials = (username, password)

    def authenticate_request(self, request: RequestOptions):
        request.auth = self.userCredentials
