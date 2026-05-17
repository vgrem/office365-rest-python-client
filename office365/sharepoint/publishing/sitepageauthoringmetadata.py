from typing import Optional

from office365.runtime.client_value import ClientValue


class SitePageAuthoringMetadata(ClientValue):
    def __init__(
        self,
        client_operation: Optional[int] = None,
        fluid_container_custom_id: Optional[str] = None,
        is_single_user_session: Optional[bool] = None,
        restored_from: Optional[str] = None,
        restore_to: Optional[str] = None,
        sequence_id: Optional[int] = None,
        session_id: Optional[str] = None,
    ):
        self.ClientOperation = client_operation
        self.FluidContainerCustomId = fluid_container_custom_id
        self.IsSingleUserSession = is_single_user_session
        self.RestoredFrom = restored_from
        self.RestoreTo = restore_to
        self.SequenceId = sequence_id
        self.SessionId = session_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageAuthoringMetadata"
