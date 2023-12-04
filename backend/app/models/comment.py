from datetime import datetime
import uuid
from sqlmodel import Field

from graphemy import MyModel, dl, get_one, get_list


class Comment(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    non_compliance_id: int
    comment: str
    created_by: str
    created_at: datetime

    @dl("NonCompliance", False)
    async def non_compliance(self, info, parameters):
        return await info.context["dl_non_compliances"].load(
            self.non_compliance_id, parameters
        )


async def dl_comment(keys: list[tuple]) -> Comment.schema:
    return await get_one(Comment, keys)


async def dl_comment_non_compliances(keys: list[tuple]) -> list[Comment.schema]:
    return await get_list(Comment, keys, "non_compliance_id")
