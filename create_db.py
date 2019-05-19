from orm.base import Base
from orm.orm import engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
