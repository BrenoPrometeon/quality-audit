from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Priority(MyModel, table=True):
    id: str = Field(primary_key=True)
    description: str