from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb
from office365.security.account import Account

if TYPE_CHECKING:
    from office365.security.action import Action
    from office365.security.identity_provider import IdentityProvider
    from office365.security.invoke_action_result import InvokeActionResult


class IdentityAccounts(Entity):
    @odata(name="cloudSecurityIdentifier")
    @property
    def cloud_security_identifier(self) -> Optional[str]:
        """Gets the cloudSecurityIdentifier property"""
        return self.properties.get("cloudSecurityIdentifier", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="domain")
    @property
    def domain(self) -> Optional[str]:
        """Gets the domain property"""
        return self.properties.get("domain", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="onPremisesSecurityIdentifier")
    @property
    def on_premises_security_identifier(self) -> Optional[str]:
        """Gets the onPremisesSecurityIdentifier property"""
        return self.properties.get("onPremisesSecurityIdentifier", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IdentityAccounts"

    @odata(name="accounts")
    @property
    def accounts(self) -> ClientValueCollection[Account]:
        """Gets the accounts property"""
        return self.properties.get("accounts", ClientValueCollection[Account](Account))

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["SecurityIdentitiesActions.ReadWrite.All"],
        application=["SecurityIdentitiesActions.ReadWrite.All"],
    )
    def invoke_action(
        self, account_id: str, action: Action, identity_provider: IdentityProvider
    ) -> ClientResult[InvokeActionResult]:
        """invokeAction operation.

        Args:
            account_id (str):
                accountId parameter
            action (Action):
                action parameter
            identity_provider (IdentityProvider):
                identityProvider parameter
        """
        from office365.security.invoke_action_result import InvokeActionResult

        return_type = ClientResult(self.context, InvokeActionResult())
        qry = ServiceOperationQuery(
            self,
            "invokeAction",
            None,
            {"accountId": account_id, "action": action, "identityProvider": identity_provider},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
