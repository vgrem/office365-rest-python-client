from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TypeInformation:
    BaseTypeFullName: Optional[str] = None
    FullName: Optional[str] = None
    IsValueObject: Optional[bool] = None
    Methods: List[str] = field(default_factory=list)
    Properties: List[str] = field(default_factory=list)
