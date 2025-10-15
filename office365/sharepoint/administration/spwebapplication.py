from typing import Optional

from office365.sharepoint.entity import Entity


class SPWebApplication(Entity):

    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @property
    def outbound_mail_port(self) -> Optional[int]:
        """Gets the OutboundMailPort property"""
        return self.properties.get("OutboundMailPort", None)

    @property
    def outbound_mail_reply_to_address(self) -> Optional[str]:
        """Gets the OutboundMailReplyToAddress property"""
        return self.properties.get("OutboundMailReplyToAddress", None)

    @property
    def outbound_mail_sender_address(self) -> Optional[str]:
        """Gets the OutboundMailSenderAddress property"""
        return self.properties.get("OutboundMailSenderAddress", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.SPWebApplication"
