from __future__ import annotations

from dataclasses import dataclass

from office365.directory.applications.csa_star_level import CsaStarLevel
from office365.directory.applications.fed_ramp_level import FedRampLevel
from office365.directory.applications.pci_version import PciVersion
from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationSecurityCompliance(ClientValue):
    cobit: bool | None = None
    coppa: bool | None = None
    csaStar: CsaStarLevel = CsaStarLevel.none
    fedRamp: FedRampLevel = FedRampLevel.none
    ferpa: bool | None = None
    ffiec: bool | None = None
    finra: bool | None = None
    fisma: bool | None = None
    gaap: bool | None = None
    gapp: bool | None = None
    glba: bool | None = None
    hipaa: bool | None = None
    hitrust: bool | None = None
    isae3402: bool | None = None
    iso27001: bool | None = None
    iso27002: bool | None = None
    iso27017: bool | None = None
    iso27018: bool | None = None
    itar: bool | None = None
    jerichoForumCommandments: bool | None = None
    pci: PciVersion = PciVersion.none
    privacyShield: bool | None = None
    safeHarbor: bool | None = None
    soc1: bool | None = None
    soc2: bool | None = None
    soc3: bool | None = None
    sox: bool | None = None
    sp800_53: bool | None = None
    ssae16: bool | None = None
    ustr: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationSecurityCompliance"
