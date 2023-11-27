from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Date(MyModel, table=True):
    id: str = Field(primary_key=True)
    master_plan: date | None
    effective: date | None
