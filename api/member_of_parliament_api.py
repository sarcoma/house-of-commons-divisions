from api.base_api import BaseApi
from models.member_of_parliament import MemberOfParliament


class MemberOfParliamentApi(BaseApi):
    def __init__(self):
        super().__init__(MemberOfParliament)
