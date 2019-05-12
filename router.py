# Todo: Add a nesting level to manage depth
# Todo: Handle serializing nested models

from flask import Blueprint

from api.commons_division_api import CommonsDivisionApi
from api.member_of_parliament_api import MemberOfParliamentApi
from request.json_request import JsonRequest
from response.json_response import json_response

router = Blueprint('router', __name__)


@router.route('/')
@json_response
def route_list():
    return {'routes': ['/commons-division', '/member-of-parliament']}


@router.route('/commons-division')
@router.route('/commons-division/page/<int:page>')
@json_response
def commons_division_list(page=1):
    return JsonRequest.list(CommonsDivisionApi(), page)


@router.route('/commons-division/<int:commons_division_id>')
@json_response
def commons_division_detail(commons_division_id):
    return JsonRequest.detail(CommonsDivisionApi(), commons_division_id)


@router.route('/member-of-parliament')
@router.route('/member-of-parliament/page/<int:page>')
@json_response
def member_of_parliament_list(page=1):
    return JsonRequest.list(MemberOfParliamentApi(), page)


@router.route('/member-of-parliament/<int:member_of_parliament_id>')
@json_response
def member_of_parliament_detail(member_of_parliament_id):
    return JsonRequest.detail(MemberOfParliamentApi(), member_of_parliament_id)
