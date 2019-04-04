
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from orm import Base


class MemberOfParliament(Base):
    __tablename__ = 'member_of_parliament'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    party = Column(String)
    votes = relationship("Vote", back_populates='member_of_parliament')
