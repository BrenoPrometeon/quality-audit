from sqlmodel import Field

from graphemy import MyModel, get_list, dl


class AuditShift(MyModel, table=True):
    _default_mutation = True
    audit_id: int = Field(primary_key=True)
    shift_id: int = Field(primary_key=True)

    @dl("Audit")
    async def audit(self, info, parameters):
        return await info.context["dl_audits"].load(self.audit_id, parameters)

    @dl("Shift")
    async def shifts(self, info, parameters):
        return await info.context["dl_shifts"].load(self.shift_id, parameters)


async def dl_audit_shift(keys: list[tuple]) -> list[AuditShift.schema]:
    return await get_list(AuditShift, keys, "audit_id")
