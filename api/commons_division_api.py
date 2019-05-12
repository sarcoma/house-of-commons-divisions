from api.base_api import BaseApi
from models.commons_division import CommonsDivision


class CommonsDivisionApi(BaseApi):
    def __init__(self):
        super().__init__(CommonsDivision)
