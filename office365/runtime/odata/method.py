from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ODataMethod:
    Name: Optional[str] = None
    IsBeta: Optional[bool] = None
    Parameters: Optional[List[str]] = None
    ReturnTypeFullName: Optional[str] = None
