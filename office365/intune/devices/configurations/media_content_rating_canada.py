from __future__ import annotations

from office365.intune.devices.configurations.ios.general.ratingcanadamoviestype import (
    RatingCanadaMoviesType,
)
from office365.intune.devices.configurations.ios.general.ratingcanadatelevisiontype import (
    RatingCanadaTelevisionType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MediaContentRatingCanada(ClientValue):
    movieRating: RatingCanadaMoviesType = RatingCanadaMoviesType.allAllowed
    tvRating: RatingCanadaTelevisionType = RatingCanadaTelevisionType.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MediaContentRatingCanada"
