from flask import request

from drone_squadron.response.json_response import json_response


class JsonRequestHandler:
    @staticmethod
    def get(api):
        return json_response(api.get())

    @staticmethod
    def post(api):
        return json_response(api.post(request.get_json()))

    @staticmethod
    def put(api, item_id):
        return json_response(api.put(item_id, request.get_json()))

    @staticmethod
    def delete(api, item_id):
        return json_response(api.delete(item_id))

    @staticmethod
    def list(api):
        if request.method == 'POST':
            return json_response(api.post(request.get_json()))
        elif request.method == 'GET':
            return json_response(api.get())

    @staticmethod
    def detail(api, item_id):
        if request.method == 'PUT':
            return json_response(api.put(item_id, request.get_json()))
        elif request.method == 'DELETE':
            return json_response(api.delete(item_id))
        elif request.method == 'GET':
            return json_response(api.get_by_id(item_id))
