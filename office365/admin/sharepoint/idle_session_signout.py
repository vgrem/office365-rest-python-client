from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IdleSessionSignOut(ClientValue):
    """Represents the idle session sign-out policy settings for SharePoint."""

    def __init__(
        self,
        is_enabled: bool | None = None,
        sign_out_after_in_seconds: int | None = None,
        warn_after_in_seconds: int | None = None,
    ):
        self.isEnabled = is_enabled
        self.signOutAfterInSeconds = sign_out_after_in_seconds
        self.warnAfterInSeconds = warn_after_in_seconds
