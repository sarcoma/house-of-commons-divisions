import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from orm import Base


class VoteType(enum.Enum):
    aye = 'aye'
    no = 'no'
    no_vote = 'no_vote'


class Vote(Base):
    __tablename__ = 'vote'

    id = Column(Integer, primary_key=True)
    member_of_parliament_id = Column(Integer, ForeignKey('member_of_parliament.id'))
    commons_division_id = Column(Integer, ForeignKey('commons_division.id'))
    vote_type = Column(Enum(VoteType))
    commons_division = relationship("CommonsDivision", back_populates='votes')
    member_of_parliament = relationship("MemberOfParliament", back_populates='votes')

    def set_vote_type(self, vote_type):
        if VoteType[vote_type.lower()] is VoteType.aye:
            self.vote_type = VoteType.aye
        elif VoteType[vote_type.lower()] is VoteType.no:
            self.vote_type = VoteType.no
        else:
            self.vote_type = VoteType.no_vote
