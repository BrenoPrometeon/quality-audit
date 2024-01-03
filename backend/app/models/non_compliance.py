from sqlmodel import Field

from graphemy import MyModel, dl, get_one


class NonCompliance(MyModel, table=True):
    _default_mutation = True
    id: int = Field(primary_key=True)
    identifier: str 
    audit_id: int
    description: str
    priority_id: int
    action_plan: int | None
    deployment: int | None
    validation: int | None

    @dl("Audit", False)
    async def audit(self, info, parameters):
        return await info.context["dl_audit"].load(self.audit_id, parameters)

    @dl("Priorities", False)
    async def priority(self, info, parameters):
        return await info.context["dl_priority"].load(self.priority_id, parameters)

    @dl("Date", False)
    async def date_action_plan(self, info, parameters):
        return await info.context["dl_date"].load(self.action_plan, parameters)

    @dl("Date", False)
    async def date_deployment(self, info, parameters):
        return await info.context["dl_date"].load(self.deployment, parameters)

    @dl("Date", False)
    async def date_validation(self, info, parameters):
        return await info.context["dl_date"].load(self.validation, parameters)

    @dl("Comment")
    async def comments(self, info, parameters):
        return await info.context["dl_comment_non_compliances"].load(
            self.id, parameters
        )


async def dl_non_compliances(keys: list[tuple]) -> NonCompliance.schema:
    return await get_one(NonCompliance, keys)


async def dl_non_compliances_audit(keys: list[tuple]) -> NonCompliance.schema:
    return await get_one(NonCompliance, keys, "audit_id")
