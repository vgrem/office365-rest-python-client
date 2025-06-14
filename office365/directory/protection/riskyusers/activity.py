from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.runtime.client_value import ClientValue


class RiskUserActivity(ClientValue):
    """Represents the risk activites of an Azure AD user as determined by Azure AD Identity Protection."""

    def __init__(self, detail=RiskDetail()):
        self.detail = detail
