from office365.entity import Entity
from office365.onedrive.sitepages.webparts.position import WebPartPosition
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery


class WebPart(Entity):
    """Represents a specific web part instance on a SharePoint page."""

    @require_permission(
        delegated=["Sites.ReadWrite.All", "Sites.Manage.All"], application=["Sites.ReadWrite.All", "Sites.Manage.All"]
    )
    def get_position_of_web_part(self) -> ClientResult[WebPartPosition]:
        """Returns the position of the specified web part in the page."""
        return_type = ClientResult(self.context, WebPartPosition())
        qry = ServiceOperationQuery(self, "getPositionOfWebPart", return_type=return_type)
        self.context.add_query(qry)
        return return_type
