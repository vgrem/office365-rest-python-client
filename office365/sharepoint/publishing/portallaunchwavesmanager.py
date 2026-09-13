from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.portallaunchwavesetup import PortalLaunchWaveSetup


class PortalLaunchWavesManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.PortalLaunch.PortalLaunchWavesManager"

    def get_all(self) -> ClientResult[ClientValueCollection[PortalLaunchWaveSetup]]:
        """GetAll operation."""
        return_type = ClientResult(self.context, ClientValueCollection[PortalLaunchWaveSetup]())
        qry = FunctionQuery(self, "GetAll", [], return_type)
        self.context.add_query(qry)
        return return_type

    def remove(self, site_url: str) -> ClientResult[bool]:
        """Remove operation.

        Args:
            site_url (str): siteUrl parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "Remove", None, {"siteUrl": site_url}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def save_wave_setup(self, portal_launch_setup: PortalLaunchWaveSetup) -> ClientResult[PortalLaunchWaveSetup]:
        """SaveWaveSetup operation.

        Args:
            portal_launch_setup (PortalLaunchWaveSetup): portalLaunchSetup parameter
        """
        return_type = ClientResult(self.context, PortalLaunchWaveSetup())
        qry = ServiceOperationQuery(
            self, "SaveWaveSetup", None, {"portalLaunchSetup": portal_launch_setup}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
