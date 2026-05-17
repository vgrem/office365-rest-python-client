from enum import Enum


class X509CertificateRuleType(Enum):
    issuerSubject = "0"
    policyOID = "1"
    unknownFutureValue = "2"
    issuerSubjectAndPolicyOID = "3"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateRuleType"
