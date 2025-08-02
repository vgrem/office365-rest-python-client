from typing import Optional

from office365.entity import Entity


class AgreementAcceptance(Entity):
    """
    Represents the current status of a user's response to a company's customizable terms of use agreement powered by
    Azure Active Directory (Azure AD).
    """

    @property
    def agreement_file_id(self) -> Optional[str]:
        """The identifier of the agreement file accepted by the user."""
        return self.properties.get("agreementFileId", None)

    @property
    def agreement_id(self) -> Optional[str]:
        """The identifier of the agreement."""
        return self.properties.get("agreementId", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """UPN of the user when the acceptance was recorded."""
        return self.properties.get("userPrincipalName", None)
