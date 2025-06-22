from typing import Any, Dict, Optional

from requests import RequestException


class ClientRequestException(RequestException):
    """Custom exception for client requests with enhanced error handling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._error_info = self._get_error_info()
        self.args = (self.code, self.message) + args

    def _get_error_info(self) -> Dict[str, Any]:
        """Extract and parse error info from response."""
        if not getattr(self, "response", None):
            return {}

        content_type = (
            self.response.headers.get("Content-Type", "").split(";")[0].lower()
        )
        if content_type == "application/json" and self.response.content:
            try:
                payload = self.response.json()
                return payload.get("error", {})
            except ValueError:
                pass
        return {}

    @property
    def code(self) -> Optional[str]:
        return self._error_info.get("code")

    @property
    def message_lang(self) -> Optional[str]:
        msg = self._error_info.get("message")
        return msg.get("lang") if isinstance(msg, dict) else None

    @property
    def message(self) -> str:
        msg = self._error_info.get("message")
        if isinstance(msg, dict):
            return str(msg.get("value", ""))
        return str(msg or self.args[0] if self.args else "")
