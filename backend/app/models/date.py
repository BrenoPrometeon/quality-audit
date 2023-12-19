from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_one


class Date(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    forecast: date
    effective: date | None
    reason: str | None

    @dl("DateUpdates")
    async def date_updates(self, info, parameters):
        return await info.context["dl_date_updates"].load(self.id, parameters)


async def dl_date(keys: list[tuple]) -> Date.schema:
    return await get_one(Date, keys)
