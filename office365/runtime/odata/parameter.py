from dataclasses import dataclass
from typing import Optional


@dataclass
class ODataParameter:
    Name: Optional[str] = None
    ParameterTypeFullName: Optional[str] = None
