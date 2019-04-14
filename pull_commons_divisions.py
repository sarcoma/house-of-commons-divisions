import json
import re
from datetime import datetime
from json import JSONDecodeError
from time import sleep

import requests

from models.commons_division import CommonsDivision
from models.member_of_parliament import MemberOfParliament
from models.vote import Vote
from orm import session_factory
from pull_members_of_parilament import create_mps_for_date, get_member, create_mp


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


def make_commons_division(id, primary_topic):
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


def make_mp(name, party):
    return MemberOfParliament(name=name, party=party)


def make_vote(vote, mp, commons_division):
    if vote:
        vote_type = re.search(r'(?:#)(\w+?)(?:Vote)', vote['type'])
        vote_type = vote_type.group(1)
    else:
        vote_type = 'no_vote'
    vote = Vote()
    vote.set_vote_type(vote_type)
    vote.commons_division = commons_division
    vote.member_of_parliament = mp
    return vote


def pull_commons_divisions(url):
    division_data = get_data_or_retry(url)
    result = division_data['result']
    next_url = result['next']
    items = result['items']
    for item in items:
        session = session_factory()
        division_url = get_about_url(item, '/resources/', '/commonsdivisions/id/')
        division_id = int(re.search('(\d+).json$', division_url).group(1))
        found_commons_division = session.query(CommonsDivision) \
            .filter(CommonsDivision.division_id == division_id) \
            .one_or_none()
        if not found_commons_division:
            division_data = get_data_or_retry(division_url)
            print('Fetching: ' + division_url)
            result = division_data['result']
            primary_topic = result['primaryTopic']
            commons_division = make_commons_division(division_id, primary_topic)
            session.add(commons_division)
            votes = primary_topic['vote']
            all_mps = set(create_mps_for_date(commons_division.date, session))
            mps_who_voted = set()
            for vote in votes:
                # Todo: Can pull additional info from _about: http://eldaddp.azurewebsites.net/members/4082
                member_about_url = vote['member'][0]['_about']
                member_id = re.search('\d+$', member_about_url).group(0)
                query = session \
                    .query(MemberOfParliament) \
                    .filter(
                    MemberOfParliament.member_id == member_id,
                )
                mp = query.one_or_none()
                if not mp:
                    member = get_member(member_id)
                    mp = create_mp(member, session)
                mps_who_voted.add(mp)
                session.add(make_vote(vote, mp, commons_division))

            for mp in all_mps - mps_who_voted:
                session.add(make_vote(None, mp, commons_division))

        session.commit()

    return next_url


if __name__ == '__main__':
    # drop_all()
    next_url = 'http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=0'
    while True:
        print('Fetching: ' + next_url)
        next_url = pull_commons_divisions(next_url)
        if not next_url:
            break
