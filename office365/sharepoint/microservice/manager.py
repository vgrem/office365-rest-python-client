from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class MicroServiceManager(Entity):
    @staticmethod
    def add_microservice_work_item(context, payload, minutes, properties):
        """Args:
        context (office365.sharepoint.client_context.ClientContext):
        payload (str or byte):
        minutes (int):
        properties (MicroServiceWorkItemProperties):
        """
        return_type = ClientResult(context)
        payload = {"payLoad": payload, "minutes": minutes, "properties": properties}
        manager = MicroServiceManager(context)
        qry = ServiceOperationQuery(manager, "AddMicroserviceWorkItem", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.MicroService.MicroServiceManager"

    def delete_microservice_work_item(self, work_item_id: UUID) -> ClientResult[bool]:
        """DeleteMicroserviceWorkItem operation.

        Args:
            work_item_id (UUID): workItemId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(
            self, "DeleteMicroserviceWorkItem", None, {"workItemId": work_item_id}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def delete_microservice_work_item_by_content_db_id(
        self, content_database_id: UUID, site_id: UUID, work_item_id: UUID
    ) -> ClientResult[bool]:
        """DeleteMicroserviceWorkItemByContentDbId operation.

        Args:
            content_database_id (UUID): contentDatabaseId parameter
            site_id (UUID): siteId parameter
            work_item_id (UUID): workItemId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(
            self,
            "DeleteMicroserviceWorkItemByContentDbId",
            None,
            {"contentDatabaseId": content_database_id, "siteId": site_id, "workItemId": work_item_id},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_service_internal_urls(self, service: str) -> ClientResult[StringCollection]:
        """GetServiceInternalUrls operation.

        Args:
            service (str): service parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetServiceInternalUrls", [service], return_type)
        self.context.add_query(qry)
        return return_type

    def get_service_urls(self, service: str) -> ClientResult[StringCollection]:
        """GetServiceUrls operation.

        Args:
            service (str): service parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetServiceUrls", [service], return_type)
        self.context.add_query(qry)
        return return_type
