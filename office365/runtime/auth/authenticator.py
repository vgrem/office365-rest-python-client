"""What a request asks of the credentials it carries.

The SharePoint and Entra authentication contexts evolved separately and share no
base class, yet every request needs the same three answers from whichever one it
holds: whether the next token must be awaited, how to sign a request
synchronously, and how to sign it on the event loop. This is that contract - a
request holds a :class:`RequestAuthenticator`, not a particular context.
"""

from __future__ import annotations

from typing import Protocol

from office365.runtime.http.request_options import RequestOptions


class RequestAuthenticator(Protocol):
    """Credentials that can sign a request, synchronously or on the event loop."""

    @property
    def is_async_token_callback(self) -> bool:
        """Whether the next token is only obtainable by awaiting."""
        ...

    def authenticate_request(self, request: RequestOptions) -> None:
        """Sign ``request`` with the token the next send would carry."""
        ...

    async def authenticate_request_async(self, request: RequestOptions) -> None:
        """Sign ``request`` on the event loop, awaiting the token when it is async."""
        ...
