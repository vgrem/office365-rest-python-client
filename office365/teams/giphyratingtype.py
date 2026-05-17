from enum import Enum


class GiphyRatingType(Enum):
    strict = "0"
    moderate = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.GiphyRatingType"
