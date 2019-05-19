from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

from orm.base import Base


class CommonsDivision(Base):
    __tablename__ = 'commons_division'

    id = Column(Integer, primary_key=True)
    division_id = Column(Integer, unique=True)
    uin = Column(String, unique=True)
    title = Column(String, index=True)
    session = Column(String)
    division_number = Column(Integer)
    date = Column(Date, index=True)
    deferred_vote = Column(Boolean)
    non_eligible = Column(Integer)
    suspended = Column(Integer)
    did_not_vote = Column(Integer)
    error_vote = Column(Integer)
    margin = Column(Integer)
    member_of_parliament = relationship("Vote", back_populates='commons_division')

    def to_dict(self, with_votes=False):
        data = dict(
            id=self.id,
            division_id=self.division_id,
            uin=self.uin,
            title=self.title,
            session=self.session,
            division_number=self.division_number,
            date=self.date,
            deferred_vote=self.deferred_vote,
            non_eligible=self.non_eligible,
            suspended=self.suspended,
            did_not_vote=self.did_not_vote,
            error_vote=self.error_vote,
            margin=self.margin
        )
        if with_votes and isinstance(self.member_of_parliament, InstrumentedList):
            data['votes'] = [{
                'vote': vote.vote_type.value,
                'member_of_parliament': {
                    'name': vote.member_of_parliament.name,
                    'party': vote.member_of_parliament.party,
                    'constituency': vote.member_of_parliament.constituency
                }
            } for vote in self.member_of_parliament]
        return data

    def __repr__(self):
        return "<%s %r>" % (self.__class__, self.to_dict())
