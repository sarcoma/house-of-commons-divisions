from abc import ABCMeta

from commons_divisions.orm.base import Base
from commons_divisions.orm.orm import session_factory


class BaseApi(metaclass=ABCMeta):

    def __init__(self, model: Base):
        self.model = model
        self.session = session_factory()

    def get_list(self):
        data = self.session.query(self.model).all()
        return [row.to_dict() for row in data]

    def get_paginated_list(self, page=1, limit=25):
        data = self.session.query(self.model).all()[limit * page - limit:limit * page]
        total = self.session.query(self.model).count()
        return {
            "data": [row.to_dict() for row in data],
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
            }
        }

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
