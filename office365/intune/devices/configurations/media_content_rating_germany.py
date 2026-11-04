from __future__ import annotations

from office365.intune.devices.configurations.ios.ratinggermanymoviestype import (
    RatingGermanyMoviesType,
)
from office365.intune.devices.configurations.ios.ratinggermanytelevisiontype import (
    RatingGermanyTelevisionType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MediaContentRatingGermany(ClientValue):
    movieRating: RatingGermanyMoviesType = RatingGermanyMoviesType.allAllowed
    tvRating: RatingGermanyTelevisionType = RatingGermanyTelevisionType.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MediaContentRatingGermany"
