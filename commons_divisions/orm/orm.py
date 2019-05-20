from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from commons_divisions.models import commons_division
from commons_divisions.models import member_of_parliament
from commons_divisions.models import vote

from commons_divisions.orm.base import Base

engine = create_engine(
    'sqlite:///./commons-divisions.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

Session = sessionmaker(bind=engine)


def drop_all():
    Base.metadata.drop_all(engine)


def session_factory():
    Base.metadata.create_all(engine)
    return Session()
