from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union, cast

from typing_extensions import Self

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_object import ClientObject
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.entity import EntityPath
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class Entity(ClientObject):
    """SharePoint specific entity"""

    def execute_query_with_incremental_retry(self, max_retry: int = 5) -> Self:
        """
        Execute query with incremental retry handling for throttling requests

        Args:
            max_retry: Maximum number of retry attempts (default: 5)

        Returns:
            self: Supports method chaining
        """
        self.context.execute_query_with_incremental_retry(max_retry)
        return self

    def execute_batch(
        self,
        items_per_batch: int = 100,
        success_callback: Optional[
            Callable[[List[Union[ClientObject, ClientResult]]], None]
        ] = None,
    ) -> Self:
        """
        Construct and submit a batch request to the server

        Args:
            items_per_batch: Number of items per batch (default: 100)
            success_callback: Callback function for successful batch execution

        Returns:
            self: Supports method chaining
        """
        return self.context.execute_batch(items_per_batch, success_callback)

    def with_credentials(
        self, credentials: Union[UserCredential, ClientCredential]
    ) -> Self:
        """
        Initialize authentication with user or client credentials

        Args:
            credentials: Authentication credentials

        Returns:
            self: Supports method chaining
        """
        self.context.with_credentials(credentials)
        return self

    def with_client_certificate(
        self,
        tenant: str,
        client_id: str,
        thumbprint: str,
        cert_path: Optional[str] = None,
        private_key: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        passphrase: Optional[str] = None,
    ) -> Self:
        """
        Creates authenticated SharePoint context via certificate credentials

        :param str tenant: Tenant name
        :param str or None cert_path: Path to A PEM encoded certificate private key.
        :param str or None private_key: A PEM encoded certificate private key.
        :param str thumbprint: Hex encoded thumbprint of the certificate.
        :param str client_id: The OAuth client id of the calling application.
        :param list[str] or None scopes:  Scopes requested to access a protected API (a resource)
        :param str passphrase: Passphrase if the private_key is encrypted
        """
        self.context.with_client_certificate(
            tenant, client_id, thumbprint, cert_path, private_key, scopes, passphrase
        )
        return self



    def delete_object(self) -> Self:
        """
        Delete the SharePoint entity

        Returns:
            self: Supports method chaining
        """
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
        return self

    def update(self, *args: Any) -> Self:
        """
        Update the SharePoint entity

        Returns:
            self: Supports method chaining
        """
        qry = UpdateEntityQuery(self)
        self.context.add_query(qry)
        return self

    @property
    def context(self) -> ClientContext:
        """Gets the client context associated with this object.

        Returns:
            ClientContext: The SharePoint client context

        Raises:
            ValueError: If the context is not initialized
        """
        from office365.sharepoint.client_context import ClientContext

        if self._context is None:
            raise ValueError("Client context is not initialized")
        return cast(ClientContext, self._context)

    @property
    def entity_type_name(self) -> str:
        """Get the entity type name"""
        if self._entity_type_name is None:
            self._entity_type_name = ".".join(["SP", type(self).__name__])
        return self._entity_type_name

    @property
    def property_ref_name(self) -> str:
        return "Id"

    def set_property(self, name: str, value: Any, persist_changes: bool = True) -> Self:
        """
        Set a property value

        Args:
            name: Property name
            value: Property value
            persist_changes: Whether to persist changes

        Returns:
            self: Supports method chaining
        """
        super(Entity, self).set_property(name, value, persist_changes)
        if name == self.property_ref_name:
            if self.resource_path is None:
                if self.parent_collection:
                    self._resource_path = EntityPath(
                        value, self.parent_collection.resource_path
                    )
            else:
                self._resource_path.patch(value)
        return self
