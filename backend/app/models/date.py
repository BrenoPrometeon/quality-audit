from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Date(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: int = Field(primary_key=True)
    master_plan: str | None
    effective: str | None
    created_by: str
    created_at: date
    modified_by: str
    modified_at: date

async def dl_date(keys: list[tuple]) -> Date.schema:
    return await get_one(Date, keys)