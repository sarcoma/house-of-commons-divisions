from abc import ABCMeta

from flask import request

from commons_divisions.orm.base import Base
from commons_divisions.orm.orm import session_factory


class BaseApi(metaclass=ABCMeta):

    def __init__(self, model: Base):
        self.model = model
        self.session = session_factory()

    def get_list(self):
        filters = self._get_filters_from_params()
        data = self._filter_results(filters)

        return [row.to_dict() for row in data]

    def get_paginated_list(self, page=1, limit=25):
        filters = self._get_filters_from_params()
        data = self._filter_results(filters)[limit * page - limit:limit * page]
        total = self._filter_results(filters).count()

        return {
            "data": [row.to_dict() for row in data],
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
            }
        }

    def _get_filters_from_params(self):
        filter_param = request.args.get('filter', None)
        if not filter_param:
            return {}
        return {k: v for k, v in [x.split(':') for x in filter_param.split(',')]}

    def _filter_results(self, filters):
        data = self.session.query(self.model)
        for search_term in [getattr(self.model, attr).like('%%%s%%' % value) for attr, value in filters.items()]:
            data = data.filter(search_term)
        return data

    def get_detail_by_id(self, item_id):
        data = self.session.query(self.model).filter(self.model.id == item_id).first()
        return data.to_dict()

    def post(self, data):
        item = self.model(**data)
        self.session.add(item)
        self.session.commit()
        return item.to_dict()

    def put(self, item_id, data):
        item = self.session.query(self.model).filter_by(self.model.id == item_id).first()
        item.update(**data)
        self.session.commit()
        return item.to_dict()

    def delete(self, item_id):
        item = self.session.query(self.model).filter_by(self.model.id == item_id).first()

        if not item:
            return False

        item.delete()
        self.session.commit()

        return True
