from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class DateUpdates(MyModel, table=True):
    id: str = Field(primary_key=True)
    date_id: str
    new_date: str
    reason: str