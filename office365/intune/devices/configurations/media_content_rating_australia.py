from __future__ import annotations

from office365.intune.devices.configurations.ios.general.ratingaustraliamoviestype import (
    RatingAustraliaMoviesType,
)
from office365.intune.devices.configurations.ios.general.ratingaustraliatelevisiontype import (
    RatingAustraliaTelevisionType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MediaContentRatingAustralia(ClientValue):
    movieRating: RatingAustraliaMoviesType = RatingAustraliaMoviesType.allAllowed
    tvRating: RatingAustraliaTelevisionType = RatingAustraliaTelevisionType.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MediaContentRatingAustralia"
