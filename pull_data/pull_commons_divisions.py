import json
import re
from datetime import datetime
from json import JSONDecodeError
from time import sleep

import requests

from models.commons_division import CommonsDivision
from models.member_of_parliament import MemberOfParliament
from models.vote import Vote
from orm.orm import session_factory
from pull_data.pull_members_of_parilament import create_mps_for_date, get_member, create_mp


class MPNotFound(Exception):
    pass


def get_data(url):
    try:
        response = requests.get(url)
        return json.loads(response.content)
    except JSONDecodeError:
        print('Error: %s' % JSONDecodeError)
        return None


def get_data_or_retry(url):
    data = False
    while not data:
        data = get_data(url)
        if not data:
            print('Retrying: %s' % url)
            for i in range(3):
                print('.', end='')
                sleep(1)
            print('\n')

    return data


def get_about_url(item, replace, endpoint):
    url = item['_about']
    url = re.sub(
        r'http://data\.parliament\.uk' + replace,
        'http://eldaddp.azurewebsites.net%s' % endpoint,
        url
    )
    return url + '.json'


def make_commons_division(id, commons_division_data):
    primary_topic = get_primary_topic(commons_division_data)
    data = {
        'division_id': id,
        'uin': primary_topic['uin'],
        'title': primary_topic['title'],
        'session': primary_topic['session'][0],
        'division_number': primary_topic['divisionNumber'],
        'date': datetime.strptime(primary_topic['date']['_value'], "%Y-%m-%d"),
        'deferred_vote': primary_topic['DeferredVote'],
        'non_eligible': primary_topic['Noneligiblecount'][0]['_value'],
        'suspended': primary_topic['Suspendedorexpelledvotescount'][0]['_value'],
        'did_not_vote': primary_topic['Didnotvotecount'][0]['_value'],
        'error_vote': primary_topic['Errorvotecount'][0]['_value'],
        'margin': primary_topic['Margin'][0]['_value']
    }
    return CommonsDivision(**data)


def make_vote(vote, mp, commons_division):
    try:
        if vote:
            vote_type = re.search(r'(?:#)(\w+?)(?:Vote)', vote['type'])
            vote_type = vote_type.group(1)
        else:
            vote_type = 'no_vote'
    except AttributeError:
        vote_type = 'no_vote'
    vote = Vote()
    vote.set_vote_type(vote_type)
    vote.commons_division = commons_division
    vote.member_of_parliament = mp
    return vote


def pull_commons_divisions(url):
    commons_division_data_list, next_url = get_commons_divisions_list(url)
    for commons_division_data in commons_division_data_list:
        session = session_factory()
        division_url = get_division_url(commons_division_data)
        division_id = get_division_id(division_url)
        commons_division = find_commons_division(division_id, session)
        if not commons_division:
            save_commons_division(division_id, division_url, session)

        session.commit()

    return next_url


def get_division_id(division_url):
    division_id = int(re.search('(\d+).json$', division_url).group(1))
    return division_id


def get_division_url(commons_division_data):
    division_url = get_about_url(commons_division_data, '/resources/', '/commonsdivisions/id/')
    return division_url


def save_commons_division(division_id, division_url, session):
    commons_division, votes = get_commons_division(division_id, division_url)
    session.add(commons_division)

    save_votes(commons_division, votes, session)


def get_votes(commons_division_data):
    return commons_division_data['result']['primaryTopic']['vote']


def get_primary_topic(commons_division_data):
    return commons_division_data['result']['primaryTopic']


def get_commons_division(division_id, division_url):
    commons_division_data = get_data_or_retry(division_url)
    print('Fetching Division: ' + division_url)
    commons_division = make_commons_division(division_id, commons_division_data)
    votes = get_votes(commons_division_data)
    return commons_division, votes


def save_votes(commons_division, votes, session):
    all_mps = set(create_mps_for_date(commons_division.date, session))
    mps_who_voted = set()
    for vote in votes:
        # Todo: Can pull additional info from _about: http://eldaddp.azurewebsites.net/members/4082
        member_id, mp = find_mp(session, vote)
        if not mp:
            member = get_member(member_id)
            mp = create_mp(member, session)
            all_mps.add(mp)
        mps_who_voted.add(mp)
        session.add(make_vote(vote, mp, commons_division))
    for mp in all_mps - mps_who_voted:
        session.add(make_vote(None, mp, commons_division))


def find_mp(session, vote):
    member_about_url = vote['member'][0]['_about']
    member_id = re.search('\d+$', member_about_url).group(0)
    query = session \
        .query(MemberOfParliament) \
        .filter(
        MemberOfParliament.member_id == member_id,
    )
    mp = query.one_or_none()
    return member_id, mp


def find_commons_division(division_id, session):
    commons_division_data = session.query(CommonsDivision) \
        .filter(CommonsDivision.division_id == division_id) \
        .one_or_none()
    return commons_division_data


def get_commons_divisions_list(url):
    division_data = get_data_or_retry(url)
    result = division_data['result']
    next_url = result['next']
    items = result['items']
    return items, next_url


if __name__ == '__main__':
    next_url = 'http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=0'
    while True:
        print('Fetching: ' + next_url)
        next_url = pull_commons_divisions(next_url)
        if not next_url:
            break
