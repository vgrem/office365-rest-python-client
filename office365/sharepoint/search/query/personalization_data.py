from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity import Entity


class QueryPersonalizationData(Entity):
    """Contains a unique identifier for the current user who is executing a search query"""

    def __init__(self, context, user_id):
        """Args:
            user_id (str):
        """
        static_path = ServiceOperationPath(
            "Microsoft.SharePoint.Client.Search.Query.QueryPersonalizationData", {"guidUserIdString": user_id}
        )
        super().__init__(context, static_path)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Client.Search.Query.QueryPersonalizationData"
