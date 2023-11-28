from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_one


class Comment(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: int = Field(primary_key=True)
    non_compliance_id: int
    comment: str
    created_by: str
    created_at: date
    modified_by: str
    modified_at: date
    
    @dl('NonCompliance', False)
    async def non_compliance(self, info, parameters):
        return await info.context['dl_non_compliance'].load(
            self.non_compliance_id, parameters
        )

async def dl_comment(keys: list[tuple]) -> Comment.schema:
    return await get_one(Comment, keys)