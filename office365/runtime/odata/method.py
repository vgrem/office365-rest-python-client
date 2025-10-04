from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MethodInformation:
    """Represents an executable OData operation (function/action).

    Attributes:
        Name: Method name as defined in OData metadata
        IsBeta: Whether this is a preview/beta method
        Parameters: List of accepted parameter names
        ReturnTypeFullName: Fully qualified return type name
    """

    Name: Optional[str] = None
    IsBeta: Optional[bool] = None
    Parameters: List[str] = list
    ReturnTypeFullName: Optional[str] = None
