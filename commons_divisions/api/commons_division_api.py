from sqlalchemy.orm import joinedload

from commons_divisions.api.base_api import BaseApi
from commons_divisions.models.commons_division import CommonsDivision


class CommonsDivisionApi(BaseApi):
    def __init__(self):
        super().__init__(CommonsDivision)

    def get_paginated_list(self, page=1, limit=25):
        filters = self._get_filters_from_params()
        data = self._filter_results(filters).order_by(self.model.date.desc())[limit * page - limit:limit * page]
        total = self._filter_results(filters).count()

        return {
            "data": [row.to_dict() for row in data],
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
            }
        }

    def get_detail_by_id(self, item_id):
        data = self.session.query(CommonsDivision) \
            .filter(self.model.id == item_id) \
            .options(joinedload('member_of_parliament')) \
            .first()

        return data.to_dict(with_votes=True)
