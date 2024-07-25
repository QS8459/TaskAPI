from typing import Any, List, Generic, TypeVar;
from pydantic import BaseModel
T = TypeVar("T")
class MostResponse(BaseModel, Generic[T]):
    results: List[T]
    page: int;
    size: int;
    count:int = 0;