from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.security.datasecurity.sensitivity_label import SensitivityLabel

if TYPE_CHECKING:
    from office365.security.datasecurity.process_content_batch_request import ProcessContentBatchRequest
    from office365.security.datasecurity.process_content_responses import ProcessContentResponses
    from office365.security.datasecurity.tenant_protection_scope_container import (
        TenantProtectionScopeContainer,
    )


class TenantDataSecurityAndGovernance(Entity):
    """Tenant-level container for data security and governance settings."""

    @odata(name="sensitivityLabels", navigation=True)
    @property
    def sensitivity_labels(self) -> EntityCollection[SensitivityLabel]:
        return self.properties.get(
            "sensitivityLabels",
            EntityCollection(self.context, SensitivityLabel, ResourcePath("sensitivityLabels", self.resource_path)),
        )

    @odata(name="protectionScopes", navigation=True)
    @property
    def protection_scopes(self) -> TenantProtectionScopeContainer:
        """Gets the protectionScopes property"""
        from office365.security.datasecurity.tenant_protection_scope_container import (
            TenantProtectionScopeContainer,
        )

        return self.properties.get(
            "protectionScopes",
            TenantProtectionScopeContainer(self.context, ResourcePath("protectionScopes", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TenantDataSecurityAndGovernance"

    def process_content_async(
        self, process_content_requests: ClientValueCollection[ProcessContentBatchRequest]
    ) -> ClientResult[ClientValueCollection[ProcessContentResponses]]:
        """processContentAsync operation.

        Args:
            process_content_requests (ClientValueCollection[ProcessContentBatchRequest]):
                processContentRequests parameter
        """
        from office365.security.datasecurity.process_content_responses import ProcessContentResponses

        return_type = ClientResult(self.context, ClientValueCollection(ProcessContentResponses))
        qry = ServiceOperationQuery(
            self, "processContentAsync", None, {"processContentRequests": process_content_requests}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
