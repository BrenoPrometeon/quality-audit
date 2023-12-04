from datetime import date
import strawberry

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from .dependencies import settings

from graphemy import MyGraphQLRouter, MyModel

engine = create_engine(settings.database_url)


class Query:
    pass


class Mutation:
    @strawberry.mutation
    async def hello(self, info) -> str:
        return "world"


app = FastAPI()

graphql_app = MyGraphQLRouter(
    query=Query,
    mutation=Mutation,
    engine=engine,
    folder="./app/models",
)
app.include_router(graphql_app, prefix="/graphql")

MyModel.metadata.create_all(engine)


with Session(engine) as session:
    session.commit()
