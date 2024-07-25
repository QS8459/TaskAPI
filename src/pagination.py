from pydantic.dataclasses import dataclass;
from fastapi import Query;

from pydantic.types import Enum;

class SortEnum(Enum):
    ASC = "asc";
    DESC = "desc";


@dataclass
class Pagination():
    perPage: int;
    page: int;
    order: int;

def pagination_param(
        page:int = Query(ge = 1, required = False, default = 1, le = 500000),
        perPage: int = Query(ge = 1, le = 100, required = False, defautl = 10),
        order: SortEnum = SortEnum.DESC
):
    return Pagination(perPage = perPage, page = page, order = order);