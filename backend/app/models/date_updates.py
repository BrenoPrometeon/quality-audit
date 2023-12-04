from datetime import datetime, date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class DateUpdates(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: int = Field(primary_key=True)
    date_id: int
    new_date: date
    reason: str
    modified_by: str
    modified_at: datetime

    @dl("Date", False)
    async def date(self, info, parameters):
        return await info.context["dl_date"].load(self.date_id, parameters)


async def dl_date_update(keys: list[tuple]) -> DateUpdates.schema:
    return await get_one(DateUpdates, keys)


async def dl_date_updates(keys: list[tuple]) -> list[DateUpdates.schema]:
    return await get_list(DateUpdates, keys, "date_id")
