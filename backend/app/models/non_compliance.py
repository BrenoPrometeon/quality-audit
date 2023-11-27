from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class NonCompliance(MyModel, table=True):
    id: str = Field(primary_key=True)
    audit_id: str
    description: str
    priority_id: str
    action_plan: str | None
    deployment: str | None
    status_id: str | None
    validate: str | None
    evidence: str | None
