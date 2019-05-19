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
    commons_division = relationship("Vote", back_populates='member_of_parliament')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "clerks_id": self.clerks_id,
            "dods_id": self.dods_id,
            "member_id": self.member_id,
            "pims_id": self.pims_id,
            "full_title": self.full_title,
            "date_of_birth": self.date_of_birth,
            "date_of_death": self.date_of_death,
            "gender": self.gender,
            "party": self.party,
            "member_since": self.member_since,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "constituency": self.constituency,
        }

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
