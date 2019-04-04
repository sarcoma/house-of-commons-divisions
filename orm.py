from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///commons-divisions.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


def drop_all():
    Base.metadata.drop_all(engine)


def session_factory():
    Base.metadata.create_all(engine)
    return Session()
