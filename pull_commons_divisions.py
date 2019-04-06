import json
import re
from datetime import datetime

import requests

from models.commons_division import CommonsDivision
from models.member_of_parliament import MemberOfParliament
from models.vote import Vote
from orm import session_factory, drop_all


def getData(url):
    response = requests.get("%s.json" % url)
    return json.loads(response.content)


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


def find_mp(name, party):

    return MemberOfParliament(name=name, party=party)


def make_vote(vote, mp, commons_division):
    vote_type = re.search(r'(?:#)(\w+?)(?:Vote)', vote['type'])
    vote_type = vote_type.group(1)
    vote = Vote()
    vote.set_vote_type(vote_type)
    vote.commons_division = commons_division
    vote.member_of_parliament = mp
    return vote


if __name__ == '__main__':
    drop_all()
    data = getData('http://eldaddp.azurewebsites.net/commonsdivisions')
    result = data['result']
    items = result['items']

    for item in items:
        session = session_factory()
        url = item['_about']
        url = re.sub(
            r'http://data\.parliament\.uk/resources/',
            'http://eldaddp.azurewebsites.net/commonsdivisions/id/',
            url
        )
        data = getData(url)
        result = data['result']
        primary_topic = result['primaryTopic']
        commons_division = make_commons_division(primary_topic)
        session.add(commons_division)
        votes = primary_topic['vote']
        for vote in votes:
            mp = find_mp(vote['memberPrinted']['_value'], vote['memberParty'])
            session.add(mp)
            session.add(make_vote(vote, mp, commons_division))

        session.commit()
