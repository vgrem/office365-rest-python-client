from datetime import datetime

from office365.runtime.client_value import ClientValue


class LockFileData(ClientValue):
    def __init__(self, lock_expire_time_stamp: datetime = datetime.min, lock_id: str = None):
        self.lock_expire_time_stamp = lock_expire_time_stamp
        self.lock_id = lock_id
