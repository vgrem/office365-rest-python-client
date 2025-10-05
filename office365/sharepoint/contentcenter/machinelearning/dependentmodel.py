from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPDependentModel(ClientValue):

    def __init__(
        self,
        last_refereshed_time_utc: datetime = None,
        model_id: str = None,
        model_type: str = None,
    ):
        self.LastRefereshedTimeUtc = last_refereshed_time_utc
        self.ModelId = model_id
        self.ModelType = model_type

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPDependentModel"
