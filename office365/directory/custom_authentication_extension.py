from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_behavior_on_error import (  # noqa: E501
    CustomExtensionBehaviorOnError,
)
from office365.entity import Entity
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.configuration.validation import AuthenticationConfigurationValidation


class CustomAuthenticationExtension(Entity):
    @odata(name="behaviorOnError")
    @property
    def behavior_on_error(self) -> CustomExtensionBehaviorOnError:
        """Gets the behaviorOnError property"""
        return self.properties.get("behaviorOnError", CustomExtensionBehaviorOnError())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAuthenticationExtension"

    def validate_authentication_configuration(self) -> ClientResult[AuthenticationConfigurationValidation]:
        """validateAuthenticationConfiguration operation."""
        from office365.directory.authentication.configuration.validation import AuthenticationConfigurationValidation

        return_type = ClientResult(self.context, AuthenticationConfigurationValidation())
        qry = ServiceOperationQuery(self, "validateAuthenticationConfiguration", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
