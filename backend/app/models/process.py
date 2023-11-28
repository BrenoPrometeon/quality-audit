from sqlmodel import Field

from graphemy import MyModel, get_one


class Process(MyModel, table=True):
    id: int = Field(primary_key=True)
    description: str

async def dl_process(keys: list[tuple]) -> Process.schema:
    return await get_one(Process, keys)