from sqlalchemy.orm import joinedload

from commons_divisions.api.base_api import BaseApi
from commons_divisions.models.commons_division import CommonsDivision


class CommonsDivisionApi(BaseApi):
    def __init__(self):
        super().__init__(CommonsDivision)

    def get_detail_by_id(self, item_id):
        data = self.session.query(CommonsDivision) \
            .filter(self.model.id == item_id) \
            .options(joinedload('member_of_parliament')) \
            .first()

        return data.to_dict(with_votes=True)
