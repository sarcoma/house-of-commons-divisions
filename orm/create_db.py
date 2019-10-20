from orm.orm import engine
from orm.base import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
