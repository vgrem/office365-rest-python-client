from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.activities_container import (
        ActivitiesContainer,
    )
    from office365.directory.identitygovernance.user_protection_scope_container import (
        UserProtectionScopeContainer,
    )
    from office365.security.datasecurity.process_content_request import ProcessContentRequest
    from office365.security.datasecurity.process_content_response import ProcessContentResponse


class UserDataSecurityAndGovernance(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserDataSecurityAndGovernance"

    @odata(name="activities", navigation=True)
    @property
    def activities(self) -> ActivitiesContainer:
        """Gets the activities property"""
        from office365.directory.identitygovernance.activities_container import (
            ActivitiesContainer,
        )

        return self.properties.get(
            "activities", ActivitiesContainer(self.context, ResourcePath("activities", self.resource_path))
        )

    @odata(name="protectionScopes", navigation=True)
    @property
    def protection_scopes(self) -> UserProtectionScopeContainer:
        """Gets the protectionScopes property"""
        from office365.directory.identitygovernance.user_protection_scope_container import (
            UserProtectionScopeContainer,
        )

        return self.properties.get(
            "protectionScopes",
            UserProtectionScopeContainer(self.context, ResourcePath("protectionScopes", self.resource_path)),
        )

    @require_permission(
        delegated=["Content.Process.User", "Content.Process.All"],
        application=["Content.Process.User", "Content.Process.All"],
    )
    def process_content(self, content_to_process: ProcessContentRequest) -> ClientResult[ProcessContentResponse]:
        """processContent operation.

        Args:
            content_to_process (ProcessContentRequest):
                contentToProcess parameter
        """
        from office365.security.datasecurity.process_content_response import ProcessContentResponse

        return_type = ClientResult(self.context, ProcessContentResponse())
        qry = ServiceOperationQuery(
            self, "processContent", None, {"contentToProcess": content_to_process}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
