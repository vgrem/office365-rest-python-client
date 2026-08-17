from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.scope import AccessReviewScope
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class PrincipalResourceMembershipsScope(AccessReviewScope):
    principalScopes: ClientValueCollection[AccessReviewScope] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewScope)
    )
    resourceScopes: ClientValueCollection[AccessReviewScope] = field(
        default_factory=lambda: ClientValueCollection(AccessReviewScope)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrincipalResourceMembershipsScope"
