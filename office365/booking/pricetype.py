from enum import Enum


class BookingPriceType(Enum):
    undefined = "0"
    fixedPrice = "1"
    startingAt = "2"
    hourly = "3"
    free = "4"
    priceVaries = "5"
    callUs = "6"
    notSet = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingPriceType"
