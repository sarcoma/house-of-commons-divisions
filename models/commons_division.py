from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from orm import Base


class CommonsDivision(Base):
    __tablename__ = 'commons_division'

    id = Column(Integer, primary_key=True)
    uin = Column(String, unique=True)
    title = Column(String)
    session = Column(String)
    division_number = Column(Integer)
    date = Column(Date)
    deferred_vote = Column(Boolean)
    non_eligible = Column(Integer)
    suspended = Column(Integer)
    did_not_vote = Column(Integer)
    error_vote = Column(Integer)
    margin = Column(Integer)
    votes = relationship('Vote', back_populates='commons_division')
