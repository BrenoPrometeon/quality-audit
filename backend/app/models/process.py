from sqlmodel import Field

from graphemy import MyModel, get_one, dl


class Process(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: int = Field(primary_key=True)
    description: str

    @dl("Audit")
    async def audits(self, info, parameters):
        return await info.context["dl_audit_process"].load(self.id, parameters)


async def dl_process(keys: list[tuple]) -> Process.schema:
    return await get_one(Process, keys)
