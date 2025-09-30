from office365.runtime.client_value import ClientValue


class SitePageAuthoringMetadata(ClientValue):

    def __init__(
        self,
        client_operation: int = None,
        fluid_container_custom_id: str = None,
        is_single_user_session: bool = None,
        restored_from: str = None,
        restore_to: str = None,
        sequence_id: int = None,
        session_id: str = None,
    ):
        self.ClientOperation = client_operation
        self.FluidContainerCustomId = fluid_container_custom_id
        self.IsSingleUserSession = is_single_user_session
        self.RestoredFrom = restored_from
        self.RestoreTo = restore_to
        self.SequenceId = sequence_id
        self.SessionId = session_id
