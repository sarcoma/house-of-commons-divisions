from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from orm import Base


class MemberOfParliament(Base):
    __tablename__ = 'member_of_parliament'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    clerks_id = Column(Integer)
    dods_id = Column(Integer)
    member_id = Column(Integer)
    pims_id = Column(Integer)
    full_title = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(String)
    party = Column(String)
    start_date = Column(Date)
    end_data = Column(Date, nullable=True)
    constituency = Column(String)
    votes = relationship("Vote", back_populates='member_of_parliament')
