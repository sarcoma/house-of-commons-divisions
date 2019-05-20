from commons_divisions.orm.base import Base
from commons_divisions.orm.orm import engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
