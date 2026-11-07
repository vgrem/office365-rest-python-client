from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.web_application_firewall_verification_model import (
        WebApplicationFirewallVerificationModel,
    )


class WebApplicationFirewallProvider(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallProvider"

    def verify(self, host_name: str) -> WebApplicationFirewallVerificationModel:
        """verify operation.

        Args:
            host_name (str):
                hostName parameter
        """
        from office365.directory.identities.web_application_firewall_verification_model import (
            WebApplicationFirewallVerificationModel,
        )

        return_type = WebApplicationFirewallVerificationModel(self.context)
        qry = ServiceOperationQuery(self, "verify", None, {"hostName": host_name}, None, return_type)
        self.context.add_query(qry)
        return return_type
