from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional

from office365.runtime.client_result import ClientResult

# Endpoints and cmdlets documented for the preview (admin-api-endpoints-reference).
# Which parameters each cmdlet accepts is endpoint-specific; unsupported ones return 400.
ORGANIZATION_CONFIG = "OrganizationConfig"
MAILBOX = "Mailbox"
MAILBOX_FOLDER_PERMISSION = "MailboxFolderPermission"


class ExchangeCmdlets:
    """Typed wrappers; the mixin expects ``invoke`` and ``invoke_all`` from the client."""

    if TYPE_CHECKING:  # the client supplies both; declared here so the mixin checks on its own

        def invoke(
            self,
            endpoint: str,
            cmdlet: str,
            parameters: Optional[Dict[str, Any]] = None,
            anchor: Optional[str] = None,
            select: Optional[list[str]] = None,
            *,
            single: bool = False,
        ) -> ClientResult: ...

        def invoke_all(
            self,
            endpoint: str,
            cmdlet: str,
            parameters: Optional[Dict[str, Any]] = None,
            anchor: Optional[str] = None,
            select: Optional[list[str]] = None,
        ) -> Iterator[Any]: ...

    def get_organization_config(self, anchor: Optional[str] = None) -> ClientResult:
        """Queue ``Get-OrganizationConfig``; after ``execute_query()`` ``.value`` is the configuration."""
        return self.invoke(ORGANIZATION_CONFIG, "Get-OrganizationConfig", anchor=anchor, single=True)

    def get_mailboxes(
        self, result_size: int = 1000, select: Optional[list[str]] = None, anchor: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
        return self.invoke_all(MAILBOX, "Get-Mailbox", {"ResultSize": result_size}, anchor, select)

    def get_mailbox_folder_permissions(self, identity: str) -> ClientResult:
        """``identity`` is ``user@contoso.com:\\Calendar``; the routing key is the target mailbox."""
        return self._folder_permission("Get-MailboxFolderPermission", identity)

    def add_mailbox_folder_permission(self, identity: str, user: str, access_rights: list[str]) -> ClientResult:
        return self._folder_permission("Add-MailboxFolderPermission", identity, User=user, AccessRights=access_rights)

    def set_mailbox_folder_permission(self, identity: str, user: str, access_rights: list[str]) -> ClientResult:
        return self._folder_permission("Set-MailboxFolderPermission", identity, User=user, AccessRights=access_rights)

    def remove_mailbox_folder_permission(self, identity: str, user: str) -> ClientResult:
        return self._folder_permission("Remove-MailboxFolderPermission", identity, User=user)

    def _folder_permission(self, cmdlet: str, identity: str, **params: Any) -> ClientResult:
        mailbox = identity.split(":", 1)[0]
        return self.invoke(
            MAILBOX_FOLDER_PERMISSION,
            cmdlet,
            {"Identity": identity, **params},
            anchor=f"AAD-UPN:{mailbox}",
        )
