from __future__ import annotations

from typing import Callable, Dict, Optional
from urllib.parse import quote

from requests import Response
from typing_extensions import Self

from office365.azure_env import AzureEnvironment
from office365.runtime.auth.certificate import CertificateData
from office365.runtime.auth.entra.authentication_context import AuthenticationContext
from office365.runtime.client_request import ASYNC_AUTHENTICATED_FLAG, ClientRequest
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery

from .environments import ADMIN_API_VERSION, exchange_host, exchange_scope
from .query import CmdletQuery

NEXT_LINK = "@odata.nextLink"


class ExchangeAdminRequest(ClientRequest):
    """Builds and authenticates Exchange Admin API calls; reuses the library transport, retry and throttling."""

    def __init__(
        self,
        tenant_id: str,
        tenant: Optional[str] = None,
        environment: AzureEnvironment = AzureEnvironment.Global,
        token_cache=None,
        authority: Optional[str] = None,
    ):
        super().__init__()
        self._tenant_id = tenant_id
        self._environment = environment
        self._auth_context = AuthenticationContext(
            tenant=tenant or tenant_id,
            scopes=[exchange_scope(environment)],
            token_cache=token_cache,
            environment=environment,
            authority=authority,
        )
        self.beforeExecute += self.authenticate_request
        self._async_authenticate = self.authenticate_request_async

    # Credentials: the same flows as GraphRequest, with the Exchange audience.
    def with_access_token(self, token_callback: Callable[[], Dict[str, str]]) -> Self:
        self._auth_context.with_access_token(token_callback)
        return self

    def with_client_secret(self, client_id: str, client_secret: str) -> Self:
        self._auth_context.with_client_secret(client_id, client_secret)
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
        self._auth_context.with_certificate(
            client_id,
            thumbprint,
            private_key,
            public_certificate=public_certificate,
            passphrase=passphrase,
            use_sni=use_sni,
        )
        return self

    def with_device_flow(self, client_id: str) -> Self:
        self._auth_context.with_device_flow(client_id)
        return self

    def with_token_interactive(self, client_id: str, username: Optional[str] = None) -> Self:
        self._auth_context.with_token_interactive(client_id, username)
        return self

    def with_username_and_password(self, client_id: str, username: str, password: str) -> Self:
        self._auth_context.with_username_and_password(client_id, username, password)
        return self

    @property
    def authentication_context(self) -> AuthenticationContext:
        return self._auth_context

    def authenticate_request(self, request: RequestOptions) -> None:
        if getattr(request, ASYNC_AUTHENTICATED_FLAG, False):
            return
        request.set_header("Authorization", self._auth_context.acquire_token().authorization_header)

    async def authenticate_request_async(self, request: RequestOptions) -> None:
        if not self._auth_context.is_async_token_callback:
            return
        token = await self._auth_context.acquire_token_async()
        request.set_header("Authorization", token.authorization_header)
        setattr(request, ASYNC_AUTHENTICATED_FLAG, True)

    @property
    def service_root_url(self) -> str:
        return f"{exchange_host(self._environment)}/adminapi/{ADMIN_API_VERSION}/{self._tenant_id}"

    def build_request(self, query: ClientQuery) -> RequestOptions:
        if not isinstance(query, CmdletQuery):
            raise TypeError(f"Exchange Admin API only executes CmdletQuery, got {type(query).__name__}")
        if query.next_link:
            url = query.next_link
        else:
            url = f"{self.service_root_url}/{query.endpoint}"
            if query.select:
                url += "?$select=" + ",".join(quote(p, safe="") for p in query.select)
        request = RequestOptions(url, method=HttpMethod.Post, data=query.body())
        request.set_header("Content-Type", "application/json")
        if query.anchor:
            request.set_header("X-AnchorMailbox", query.anchor)
        return request

    def handle_response(self, response: Response, query: ClientQuery) -> None:
        if not isinstance(query, CmdletQuery):
            return
        payload = response.json() if response.content else {}
        envelope = payload if isinstance(payload, dict) else {}
        query.next_link = envelope.get(NEXT_LINK)
        if query.return_type is not None:
            # Every answer is wrapped in the same envelope; a caller asked for the value, not the wrapper.
            value = envelope.get("value", [])
            if query.single:
                value = value[0] if value else {}
            query.return_type.set_property("__value", value)
