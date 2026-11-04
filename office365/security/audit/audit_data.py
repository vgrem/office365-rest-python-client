from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.audit.audit_record_type_dictionary import AuditRecordTypeDictionary


@value
class AuditData(ClientValue):
    dynamicProperties: AuditRecordTypeDictionary = field(default_factory=AuditRecordTypeDictionary)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AuditData"
