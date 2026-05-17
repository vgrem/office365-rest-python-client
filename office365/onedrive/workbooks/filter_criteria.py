from __future__ import annotations

from typing import List

from office365.runtime.client_value import ClientValue


class WorkbookFilterCriteria(ClientValue):
    """Represents the filtering criteria applied to a column."""

    def __init__(
        self,
        color: str | None = None,
        dynamic_criteria: str | None = None,
        operator: str | None = None,
        values: List | None = None,
    ):
        """
        :param str color:  The color applied to the cell.
        :param str dynamic_criteria:  A dynamic formula specified in a custom filter.
        :param str operator: An operator in a cell; for example, =, >, <, <=, or <>.
        :param list values: The values that appear in the cell.
        """
        self.color = color
        self.dynamicCriteria = dynamic_criteria
        self.operator = operator
        self.values = values
