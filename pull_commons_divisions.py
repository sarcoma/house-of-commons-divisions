import json
import re
from datetime import datetime
from json import JSONDecodeError
from time import sleep

import requests

from models.commons_division import CommonsDivision
from models.member_of_parliament import MemberOfParliament
from models.vote import Vote
from orm import session_factory, drop_all
from pull_members_of_parilament import create_mps_for_date


class MPNotFound(Exception):
    pass


def getData(url):
    try:
        response = requests.get(url)
        return json.loads(response.content)
    except JSONDecodeError:
        print('Error: %s' % JSONDecodeError)
        print('Retrying: %s' % url)
        for i in range(3):
            print('.', end='')
            sleep(1)
        print('\n')
        return False


def make_commons_division(primary_topic):
    data = {
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
    vote_type = re.search(r'(?:#)(\w+?)(?:Vote)', vote['type'])
    vote_type = vote_type.group(1)
    vote = Vote()
    vote.set_vote_type(vote_type)
    vote.commons_division = commons_division
    vote.member_of_parliament = mp
    return vote


def pull_commons_divisions(url):
    data = get_data_or_retry(url)
    result = data['result']
    next_url = result['next']
    items = result['items']
    for item in items:
        session = session_factory()
        url = item['_about']
        url = re.sub(
            r'http://data\.parliament\.uk/resources/',
            'http://eldaddp.azurewebsites.net/commonsdivisions/id/',
            url
        )
        division_url = "%s.json" % url
        print(division_url)
        data = get_data_or_retry(division_url)
        result = data['result']
        primary_topic = result['primaryTopic']
        uin = primary_topic['uin']
        if not session.query(CommonsDivision).filter(CommonsDivision.uin == uin).one_or_none():
            commons_division = make_commons_division(primary_topic)
            session.add(commons_division)
            create_mps_for_date(commons_division.date, session)
            votes = primary_topic['vote']
            for vote in votes:
                query = session \
                    .query(MemberOfParliament) \
                    .filter(
                    MemberOfParliament.name == vote['memberPrinted']['_value'],
                )
                mp = query.one_or_none()
                if not mp:
                    raise MPNotFound("%s, %s" % (vote['memberPrinted']['_value'], vote['memberParty']))
                session.add(make_vote(vote, mp, commons_division))

        session.commit()

    return next_url


def get_data_or_retry(url):
    data = False
    while not data:
        data = getData(url)
    return data


if __name__ == '__main__':
    drop_all()
    next_url = 'http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=0'
    while True:
        next_url = pull_commons_divisions(next_url)
        print(next_url)
        if not next_url:
            break
