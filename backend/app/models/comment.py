from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Comment(MyModel, table=True):
    id: str = Field(primary_key=True)
    non_compliance_id: str
    comment: set
    date: date 
    author: str