from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.admin.exchange.exchange_message_trace_status import ExchangeMessageTraceStatus
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.admin.exchange.exchange_message_trace_detail import ExchangeMessageTraceDetail


class ExchangeMessageTrace(Entity):
    @odata(name="fromIP")
    @property
    def from_ip(self) -> Optional[str]:
        """Gets the fromIP property"""
        return self.properties.get("fromIP", None)

    @odata(name="messageId")
    @property
    def message_id(self) -> Optional[str]:
        """Gets the messageId property"""
        return self.properties.get("messageId", None)

    @odata(name="receivedDateTime")
    @property
    def received_date_time(self) -> datetime:
        """Gets the receivedDateTime property"""
        return self.properties.get("receivedDateTime", datetime.min)

    @odata(name="recipientAddress")
    @property
    def recipient_address(self) -> Optional[str]:
        """Gets the recipientAddress property"""
        return self.properties.get("recipientAddress", None)

    @odata(name="senderAddress")
    @property
    def sender_address(self) -> Optional[str]:
        """Gets the senderAddress property"""
        return self.properties.get("senderAddress", None)

    @odata(name="size")
    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @odata(name="subject")
    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @odata(name="toIP")
    @property
    def to_ip(self) -> Optional[str]:
        """Gets the toIP property"""
        return self.properties.get("toIP", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeMessageTrace"

    @odata(name="status")
    @property
    def status(self) -> ExchangeMessageTraceStatus:
        """Gets the status property"""
        return self.properties.get("status", ExchangeMessageTraceStatus.gettingStatus)

    def get_details_by_recipient(self, recipient_address: str) -> EntityCollection[ExchangeMessageTraceDetail]:
        """getDetailsByRecipient operation.

        Args:
            recipient_address (str):
                recipientAddress parameter
        """
        from office365.admin.exchange.exchange_message_trace_detail import ExchangeMessageTraceDetail

        return_type = EntityCollection(self.context, ExchangeMessageTraceDetail)
        qry = FunctionQuery(self, "getDetailsByRecipient", {"recipientAddress": recipient_address}, return_type)
        self.context.add_query(qry)
        return return_type
