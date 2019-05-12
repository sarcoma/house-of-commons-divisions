from flask import request


class JsonRequest:
    @staticmethod
    def get(api):
        return api.get()

    @staticmethod
    def post(api):
        return api.post(request.get_json())

    @staticmethod
    def put(api, item_id):
        return api.put(item_id, request.get_json())

    @staticmethod
    def delete(api, item_id):
        return api.delete(item_id)

    @staticmethod
    def list(api, page=1, limit=25, paginated=True):
        if request.method == 'POST':
            return api.post(request.get_json())
        elif request.method == 'GET':
            return api.get_paginated_list(page, limit) if paginated else api.get_list()

    @staticmethod
    def detail(api, item_id):
        if request.method == 'PUT':
            return api.put(item_id, request.get_json())
        elif request.method == 'DELETE':
            return api.delete(item_id)
        elif request.method == 'GET':
            return api.get_detail_by_id(item_id)
