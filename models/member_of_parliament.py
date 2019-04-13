from sqlalchemy import Column, Integer, String, Date

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
    date_of_death = Column(Date, nullable=True)
    gender = Column(String)
    party = Column(String)
    member_since = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    constituency = Column(String)
