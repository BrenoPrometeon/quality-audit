from sqlmodel import Field

from graphemy import MyModel, dl, get_one, get_list


class Audit(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    process_id: int
    date_id: int | None
    report_date_id: int | None

    @dl("Process", False)
    async def process(self, info, parameters):
        return await info.context["dl_process"].load(self.process_id, parameters)

    @dl("AuditShift")
    async def audit_shifts(self, info, parameters):
        return await info.context["dl_audit_shift"].load(self.id, parameters)

    @dl("Date", False)
    async def date_end(self, info, parameters):
        return await info.context["dl_date"].load(self.date_id, parameters)

    @dl("Date", False)
    async def date_report(self, info, parameters):
        return await info.context["dl_date"].load(self.report_date_id, parameters)


async def dl_audit(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys)


async def dl_audits(keys: list[tuple]) -> list[Audit.schema]:
    return await get_list(Audit, keys)


async def dl_audit_process(keys: list[tuple]) -> list[Audit.schema]:
    return await get_list(Audit, keys, "process_id")


async def dl_audit_date(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys, "date_id")


async def dl_audit_report(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys, "report_date_id")
