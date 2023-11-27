from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Process(MyModel, table=True):
    id: str = Field(primary_key=True)
    description: str