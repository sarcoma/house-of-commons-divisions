import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from orm.base import Base


class VoteType(enum.Enum):
    aye = 'aye'
    no = 'no'
    no_vote = 'no_vote'


class Vote(Base):
    __tablename__ = 'vote'

    member_of_parliament_id = Column(Integer, ForeignKey('member_of_parliament.id'), primary_key=True)
    commons_division_id = Column(Integer, ForeignKey('commons_division.id'), primary_key=True)
    vote_type = Column(Enum(VoteType))
    commons_division = relationship("CommonsDivision", back_populates='member_of_parliament')
    member_of_parliament = relationship("MemberOfParliament", back_populates='commons_division')

    def set_vote_type(self, vote_type):
        try:
            if VoteType[vote_type.lower()] is VoteType.aye:
                self.vote_type = VoteType.aye
            elif VoteType[vote_type.lower()] is VoteType.no:
                self.vote_type = VoteType.no
            else:
                self.vote_type = VoteType.no_vote
        except KeyError:
            self.vote_type = VoteType.no_vote

    def to_dict(self):
        return self.vote_type.value
