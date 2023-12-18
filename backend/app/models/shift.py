from sqlmodel import Field

from graphemy import MyModel, get_list, dl


class Shift(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    description: str

    @dl("Audit")
    async def audits(self, info, parameters):
        return await info.context["dl_audit_process"].load(self.id, parameters)


async def dl_shifts(keys: list[tuple]) -> list[Shift.schema]:
    return await get_list(Shift, keys)
