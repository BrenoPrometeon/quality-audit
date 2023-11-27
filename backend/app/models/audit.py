from datetime import date

from sqlmodel import Field

from graphemy import MyModel, dl, get_list, get_one


class Audit(MyModel, table=True):
    id: str = Field(primary_key=True)
    process_id: str
    end_date: date
    report_date: date

    @dl('Process', False)
    async def process(self, info, parameters):
        return await info.context['dl_process'].load(
            self.process_id, parameters
        )
    @dl('Date')
    async def process(self, info, parameters):
        return await info.context['dl_date'].load(
            self.process_id, parameters
        )



async def dl_audit(keys: list[tuple]) -> Audit.schema:
    return await get_one(Audit, keys)