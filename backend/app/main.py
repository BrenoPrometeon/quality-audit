from datetime import date
import strawberry

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from .models.audit import Audit
from .models.date import Date
from .models.date_updates import DateUpdates
from .models.process import Process
from .models.status import Status
from .models.priority import Priorities
from .models.non_compliance import NonCompliance
from .models.comment import Comment

from graphemy import MyGraphQLRouter, MyModel

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)


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
    audit_1 = Audit(
        id= 1,
        process_id= 1,
        end_date= 1,
        report_date= 2,
        created_by='Doreto',
        created_at=date(2023,5,12),
        modified_by='Breno Galdino',
        modified_at=date(2023,4,12),
    )

    process_1 = Process(
        id= 1,
        description='R&D'
    )

    date_1 = Date(
        id=1,
        master_plan='14/02/2024',
        effective='',
        created_by='Doreto',
        created_at=date(2023,5,12),
        modified_by='Breno Galdino',
        modified_at=date(2023,4,12),
    )

    date_updates_1= DateUpdates(
        id=1,
        date_id=1,
        new_date='01/12/2023',
        reason='Testando...',
        created_by='Doreto',
        created_at=date(2023,5,12),
        modified_by='Breno Galdino',
        modified_at=date(2023,4,12),
    )

    status_1 = Status(id=1, description='Incompleto')

    priority_1 = Priorities(id=1, description='Major')

    non_compliance_1 = NonCompliance(
        id=1, 
        audit_id=1,
        description='Teste Teste Teste',
        priority_id=1,
        action_plan=1,
        deployment=1,
        status_id=1,
        validation=1,
        evidence=False,
        created_by='Doreto',
        created_at=date(2023,5,12),
        modified_by='Breno Galdino',
        modified_at=date(2023,4,12),
    )
    non_compliance_2 = NonCompliance(
        id=2, 
        audit_id=1,
        description='HELLO WORLD',
        priority_id=1,
        action_plan=1,
        deployment=1,
        status_id=1,
        validation=1,
        evidence=False,
        created_by='Luana',
        created_at=date(2023,5,12),
        modified_by='Rodney',
        modified_at=date(2023,4,12),
    )
    comment_1 = Comment(
        id=1,
        non_compliance_id=1,
        comment='Aqui quem fala é seu pai',
        created_by='Doreto',
        created_at=date(2023,5,12),
        modified_by='Breno Galdino',
        modified_at=date(2023,4,12),
    )

    session.add(audit_1)
    session.add(process_1)
    session.add(date_1)
    session.add(date_updates_1)
    session.add(status_1)
    session.add(priority_1)
    session.add(non_compliance_1)
    session.add(non_compliance_2)    
    session.add(comment_1)

    session.commit()
