from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from orm.base import Base


class MemberOfParliament(Base):
    __tablename__ = 'member_of_parliament'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    clerks_id = Column(Integer)
    dods_id = Column(Integer)
    member_id = Column(Integer, index=True)
    pims_id = Column(Integer)
    full_title = Column(String, index=True)
    date_of_birth = Column(Date)
    date_of_death = Column(Date, nullable=True)
    gender = Column(String)
    party = Column(String)
    member_since = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    constituency = Column(String, index=True)
    votes = relationship("Vote", back_populates='member_of_parliament')

    def __hash__(self):
        return hash((self.id, self.member_id))

    def __eq__(self, other):
        try:
            return (self.id, self.member_id) == (other.id, other.member_id)
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return (self.id, self.member_id) != (other.id, other.member_id)
        except AttributeError:
            return NotImplemented
