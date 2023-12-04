from datetime import datetime

from sqlmodel import Field

from graphemy import MyModel, dl, get_one, get_list


class Audit(MyModel, table=True):
    _default_mutation = _delete_mutation = True
    id: int = Field(primary_key=True)
    process_id: int
    end_date: int
    report_date: int
    created_by: str
    created_at: datetime
    modified_by: str | None
    modified_at: datetime | None

    @dl("Process", False)
    async def process(self, info, parameters):
        return await info.context["dl_process"].load(self.process_id, parameters)

    @dl("Date", False)
    async def date_end(self, info, parameters):
        return await info.context["dl_date"].load(self.end_date, parameters)

    @dl("Date", False)
    async def date_report(self, info, parameters):
        return await info.context["dl_date"].load(self.report_date, parameters)


async def dl_audit(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys)


async def dl_audit_process(keys: list[tuple]) -> list[Audit.schema]:
    return await get_list(Audit, keys, "process_id")


async def dl_audit_end(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys, "end_date")


async def dl_audit_report(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys, "report_date")
