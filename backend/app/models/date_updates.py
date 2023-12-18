from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list


class DateUpdates(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    date_id: int
    new_date: date
    reason: str

    @dl("Date", False)
    async def date(self, info, parameters):
        return await info.context["dl_date"].load(self.date_id, parameters)


async def dl_date_updates(keys: list[tuple]) -> list[DateUpdates.schema]:
    return await get_list(DateUpdates, keys, "date_id")
