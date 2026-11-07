from __future__ import annotations

from typing import Any, Callable, Dict, Iterator, Optional

from typing_extensions import Self

from office365.azure_env import AzureEnvironment
from office365.runtime.auth.certificate import CertificateData
from office365.runtime.client_result import ClientResult
from office365.runtime.client_runtime_context import ClientRuntimeContext

from .cmdlets import ExchangeCmdlets
from .environments import SYSTEM_MAILBOX_GUID
from .query import CmdletQuery
from .request import ExchangeAdminRequest


def _items(payload: Any) -> list:
    """The items one page carried, already unwrapped by the request."""
    if isinstance(payload, list):
        return payload
    return [payload] if payload else []


class ExchangeAdminClient(ExchangeCmdlets, ClientRuntimeContext):
    """Exchange Online Admin API client (preview REST surface; cmdlet-style POSTs, no OData).

    Inherits retry, rate limiting, hooks, async and parallel execution from ``ClientRuntimeContext``.
    ``anchor`` is the default ``X-AnchorMailbox``: the admin UPN (delegated) or the system mailbox (app-only).
    """

    def __init__(
        self,
        tenant_id: str,
        tenant: Optional[str] = None,
        anchor: Optional[str] = None,
        token_callback: Optional[Callable[[], Dict[str, str]]] = None,
        token_cache: Any = None,
        environment: AzureEnvironment = AzureEnvironment.Global,
        authority: Optional[str] = None,
    ):
        super().__init__()
        self._tenant_id = tenant_id
        self._tenant = tenant
        self._anchor = anchor
        self._token_callback = token_callback
        self._token_cache = token_cache
        self._environment = environment
        self._authority = authority

    @staticmethod
    def system_mailbox_anchor(organization: str) -> str:
        """Routing key for app-only calls that target no mailbox; ``organization`` is a tenant ID or domain."""
        return f"APP:SystemMailbox{{{SYSTEM_MAILBOX_GUID}}}@{organization}"

    @property
    def anchor(self) -> Optional[str]:
        return self._anchor

    def pending_request(self) -> ExchangeAdminRequest:
        if self._pending_request is None:
            self._pending_request = ExchangeAdminRequest(
                tenant_id=self._tenant_id,
                tenant=self._tenant,
                environment=self._environment,
                token_cache=self._token_cache,
                authority=self._authority,
            )
            if callable(self._token_callback):
                self._pending_request.with_access_token(self._token_callback)
        return self._pending_request  # type: ignore[return-value]

    def with_client_secret(self, client_id: str, client_secret: str) -> Self:
        self.pending_request().with_client_secret(client_id, client_secret)
        return self

    def with_certificate(
        self,
        client_id: str,
        thumbprint: Optional[str] = None,
        private_key: Optional[str] = None,
        *,
        public_certificate: Optional[CertificateData] = None,
        passphrase: Optional[str] = None,
        use_sni: bool = False,
    ) -> Self:
        self.pending_request().with_certificate(
            client_id,
            thumbprint,
            private_key,
            public_certificate=public_certificate,
            passphrase=passphrase,
            use_sni=use_sni,
        )
        return self

    def with_device_flow(self, client_id: str) -> Self:
        self.pending_request().with_device_flow(client_id)
        return self

    def with_token_interactive(self, client_id: str, username: Optional[str] = None) -> Self:
        self.pending_request().with_token_interactive(client_id, username)
        return self

    def with_username_and_password(self, client_id: str, username: str, password: str) -> Self:
        """Delegated ROPC; fails under MFA or conditional access. Test tenants only."""
        self.pending_request().with_username_and_password(client_id, username, password)
        return self

    def invoke(
        self,
        endpoint: str,
        cmdlet: str,
        parameters: Optional[Dict[str, Any]] = None,
        anchor: Optional[str] = None,
        select: Optional[list[str]] = None,
        *,
        single: bool = False,
    ) -> ClientResult:
        """Queue one cmdlet call; ``execute_query()`` runs it and the result holds the value.

        A cmdlet answers a collection even when it returns one object; pass ``single=True`` when
        the cmdlet has exactly one answer and the wrapper is noise.
        """
        return self._queue(endpoint, cmdlet, parameters, anchor, select, single=single).result

    def invoke_all(
        self,
        endpoint: str,
        cmdlet: str,
        parameters: Optional[Dict[str, Any]] = None,
        anchor: Optional[str] = None,
        select: Optional[list[str]] = None,
    ) -> Iterator[Any]:
        """Run the cmdlet and follow ``@odata.nextLink`` (valid about 5 minutes) with unchanged parameters."""
        qry = self._queue(endpoint, cmdlet, parameters, anchor, select)
        while True:
            self.execute_query()
            yield from _items(qry.result.value)
            if not qry.next_link:
                return
            qry = self._queue(endpoint, cmdlet, parameters, anchor, select, next_link=qry.next_link)

    def _queue(self, endpoint, cmdlet, parameters, anchor, select, next_link=None, single=False) -> CmdletQuery:
        qry = CmdletQuery(
            self,
            endpoint,
            cmdlet,
            parameters,
            anchor=anchor or self._anchor,
            select=select,
            next_link=next_link,
            single=single,
        )
        self.add_query(qry)
        return qry
