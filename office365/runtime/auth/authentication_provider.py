from abc import ABC, abstractmethod

from office365.runtime.http.request_options import RequestOptions


class AuthenticationProvider(ABC):
    """Abstract base class for authentication providers."""

    @abstractmethod
    def authenticate_request(self, request: RequestOptions) -> None:
        """Authenticate the outgoing request.

        Args:
            request: The request to authenticate

        Raises:
            AuthenticationError: If authentication fails
        """
        pass
