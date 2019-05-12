from sqlalchemy.orm import joinedload

from api.base_api import BaseApi
from models.commons_division import CommonsDivision


class CommonsDivisionApi(BaseApi):
    def __init__(self):
        super().__init__(CommonsDivision)

    def get_detail_by_id(self, item_id):
        data = self.session.query(self.model) \
            .options(joinedload('votes')) \
            .filter(self.model.id == item_id) \
            .first()

        return data
