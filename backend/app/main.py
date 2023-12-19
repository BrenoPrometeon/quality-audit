from datetime import date
import strawberry
from typing import Annotated

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from .dependencies import settings

from graphemy import MyGraphQLRouter, MyModel
from fastapi.middleware.cors import CORSMiddleware

from .models.audit import Audit
from .models.date import Date
from .models.audit_shifts import AuditShift

engine = create_engine(settings.database_url)


class Query:
    pass


class Mutation:
    @strawberry.mutation
    async def add_audit(
        self, process_id: int, forecast: date, shifts: list[int]
    ) -> Annotated["Audit.schema", "graphemy.router"]:
        with Session(engine) as session:
            date_end = Date(forecast=forecast)
            session.add(date_end)
            session.commit()

            date_id = date_end.id

            audit = Audit(process_id=process_id, date_id=date_id)
            session.add(audit)
            session.commit()

            audit_id = audit.id
            for shift in shifts:
                audit_shift = AuditShift(audit_id=audit_id, shift_id=shift)
                session.add(audit_shift)
            session.commit()

            return Audit.schema(id=audit_id, process_id=process_id, date_id=date_id)


app = FastAPI()

graphql_app = MyGraphQLRouter(
    query=Query,
    mutation=Mutation,
    engine=engine,
    folder="./app/models",
)
app.include_router(graphql_app, prefix="/graphql")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MyModel.metadata.create_all(engine)
