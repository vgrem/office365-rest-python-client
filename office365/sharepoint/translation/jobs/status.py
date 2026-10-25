from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.translation.item_info import TranslationItemInfo
from office365.sharepoint.translation.jobs.info import TranslationJobInfo


class TranslationJobStatus(Entity):
    """The TranslationJobStatus type is used to get information about previously submitted translation jobs and
    the translation items associated with them. The type provides methods to retrieve
    TranslationJobInfo (section 3.1.5.4) and TranslationItemInfo (section 3.1.5.2) objects.
    """

    @staticmethod
    def get_all_jobs(context, return_type=None):
        if return_type is None:
            return_type = ClientResult(context, ClientValueCollection(TranslationJobInfo))
        qry = ServiceOperationQuery(TranslationJobStatus(context), "GetAllJobs", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Translation.TranslationJobStatus"

    @odata(name="Canceled")
    @property
    def canceled(self) -> Optional[int]:
        """Gets the Canceled property"""
        return self.properties.get("Canceled", None)

    @odata(name="Count")
    @property
    def count(self) -> Optional[int]:
        """Gets the Count property"""
        return self.properties.get("Count", None)

    @odata(name="Failed")
    @property
    def failed(self) -> Optional[int]:
        """Gets the Failed property"""
        return self.properties.get("Failed", None)

    @odata(name="InProgress")
    @property
    def in_progress(self) -> Optional[int]:
        """Gets the InProgress property"""
        return self.properties.get("InProgress", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="NotStarted")
    @property
    def not_started(self) -> Optional[int]:
        """Gets the NotStarted property"""
        return self.properties.get("NotStarted", None)

    @odata(name="Succeeded")
    @property
    def succeeded(self) -> Optional[int]:
        """Gets the Succeeded property"""
        return self.properties.get("Succeeded", None)

    def get_all_items(self) -> ClientResult[ClientValueCollection[TranslationItemInfo]]:
        """GetAllItems operation."""
        return_type = ClientResult(self.context, ClientValueCollection[TranslationItemInfo]())
        qry = FunctionQuery(self, "GetAllItems", [], return_type)
        self.context.add_query(qry)
        return return_type
