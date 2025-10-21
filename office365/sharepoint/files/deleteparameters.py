from office365.runtime.client_value import ClientValue


class FileDeleteParameters(ClientValue):

    def __init__(
        self,
        bypass_checked_out: bool = None,
        bypass_shared_lock: bool = None,
        e_tag_match: str = None,
    ):
        self.bypass_checked_out = bypass_checked_out
        self.bypass_shared_lock = bypass_shared_lock
        self.e_tag_match = e_tag_match
