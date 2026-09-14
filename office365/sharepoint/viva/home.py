from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.viva.home_title_region import VivaHomeTitleRegion
from office365.sharepoint.viva.targetedsitedetails import TargetedSiteDetails


class VivaHome(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.VivaHome"

    def title_region(self, viva_home_title_region: VivaHomeTitleRegion) -> Self:
        """TitleRegion operation.

        Args:
            viva_home_title_region (VivaHomeTitleRegion): vivaHomeTitleRegion parameter
        """
        qry = ServiceOperationQuery(
            self, "TitleRegion", None, {"vivaHomeTitleRegion": viva_home_title_region}, None, None
        )
        self.context.add_query(qry)
        return self

    def update_go_to_vc_button_flag(
        self, is_go_back_to_connections_button_disabled: bool
    ) -> ClientResult[TargetedSiteDetails]:
        """UpdateGoToVCButtonFlag operation.

        Args:
            is_go_back_to_connections_button_disabled (bool): isGoBackToConnectionsButtonDisabled parameter
        """
        return_type = ClientResult(self.context, TargetedSiteDetails())
        qry = ServiceOperationQuery(
            self,
            "UpdateGoToVCButtonFlag",
            None,
            {"isGoBackToConnectionsButtonDisabled": is_go_back_to_connections_button_disabled},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
