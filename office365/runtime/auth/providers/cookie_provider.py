from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Optional, Union

from office365.runtime.auth.auth_cookies import AuthCookies
from office365.runtime.auth.authentication_provider import AuthenticationProvider


class CookieAuthProvider(AuthenticationProvider):
    """Authentication provider that applies SharePoint Online browser-session cookies.

    Accepts a cookie source callback or a prebuilt AuthCookies instance and sets
    the HTTP "Cookie" header on outgoing requests. Optionally, a TTL can be supplied
    to refresh cached cookies after a specified number of seconds.
    """

    def __init__(
        self,
        cookie_source: Union[Callable[[], Dict[str, str]], AuthCookies],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        super().__init__()
        self._cookie_source = cookie_source
        self._ttl_seconds = ttl_seconds
        self._cached_auth_cookies: Optional[AuthCookies] = None
        self._acquired_at: Optional[datetime] = None

    def refresh(self) -> None:
        """Clears the cached cookies so that the next request reacquires them."""
        self._cached_auth_cookies = None
        self._acquired_at = None

    def _is_expired(self, now_utc: datetime) -> bool:
        if self._cached_auth_cookies is None:
            return True
        if self._ttl_seconds is None:
            return False
        if self._acquired_at is None:
            return True
        return now_utc >= self._acquired_at + timedelta(seconds=self._ttl_seconds)

    def _acquire_from_source(self) -> AuthCookies:
        source = self._cookie_source
        if callable(source):
            result = source()
            if isinstance(result, AuthCookies):
                cookies = result
            elif isinstance(result, dict):
                cookies = AuthCookies(result)
            else:
                raise ValueError(
                    "cookie_source must return Dict[str, str] or AuthCookies"
                )
        elif isinstance(source, AuthCookies):
            cookies = source
        else:
            raise ValueError(
                "cookie_source must be a Callable[[], Dict[str, str]] or AuthCookies"
            )

        if not cookies.is_valid:
            raise ValueError("Provided cookies are not valid for SharePoint Online.")
        return cookies

    def _ensure_cookies_cached(self) -> None:
        now_utc = datetime.now(timezone.utc)
        if self._is_expired(now_utc):
            cookies = self._acquire_from_source()
            self._cached_auth_cookies = cookies
            self._acquired_at = now_utc

    def authenticate_request(self, request) -> None:
        """Sets the Cookie header using cached or freshly acquired cookies."""
        self._ensure_cookies_cached()
        request.set_header("Cookie", self._cached_auth_cookies.cookie_header)
