from office365.runtime.auth.authentication_provider import AuthenticationProvider


class NetworkCredentialProvider(AuthenticationProvider):
    """Provides credentials for password-based authentication schemes such as basic authentication"""

    def __init__(self, username, password):
        super().__init__()
        self.userCredentials = (username, password)

    def authenticate_request(self, request):
        request.auth = self.userCredentials
