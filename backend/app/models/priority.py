from sqlmodel import Field

from graphemy import MyModel, get_one


class Priorities(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    description: str


async def dl_priority(keys: list[tuple]) -> Priorities.schema:
    return await get_one(Priorities, keys)
