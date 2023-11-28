from datetime import date

from sqlmodel import Field

from graphemy import MyModel, get_one


class Status(MyModel, table=True):
    id: int = Field(primary_key=True)
    description: str
    
async def dl_status(keys: list[tuple]) -> Status.schema:
    return await get_one(Status, keys)