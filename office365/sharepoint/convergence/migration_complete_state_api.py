from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class MigrationCompleteStateApi(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Convergence.MigrationCompleteStateApi"

    def add_state(self) -> Self:
        """AddState operation."""
        qry = ServiceOperationQuery(self, "AddState", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def is_doclib_contributor_owner_enabled(self) -> ClientResult[bool]:
        """IsDoclibContributorOwnerEnabled operation."""
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "IsDoclibContributorOwnerEnabled", [], return_type)
        self.context.add_query(qry)
        return return_type

    def is_suspended(self) -> ClientResult[bool]:
        """IsSuspended operation."""
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "IsSuspended", [], return_type)
        self.context.add_query(qry)
        return return_type
