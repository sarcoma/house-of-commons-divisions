import json
import re
from datetime import datetime

import requests


def getData(url):
    response = requests.get("%s.json" % url)
    return json.loads(response.content)


class CommonsDivision:
    def __init__(
            self,
            uin,
            title,
            session,
            division_number,
            date,
            deferred_vote,
            non_eligible,
            ayes,
            noes,
            abstained,
            suspended,
            did_not_vote,
            error_vote,
            margin,
    ):
        self.uin = uin
        self.title = title
        self.session = session
        self.division_number = int(division_number)
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.deferred_vote = deferred_vote
        self.non_eligible = int(non_eligible)
        self.ayes = int(ayes)
        self.noes = int(noes)
        self.abstained = int(abstained)
        self.suspended = int(suspended)
        self.did_not_vote = int(did_not_vote)
        self.error_vote = int(error_vote)
        self.margin = int(margin)

    def __repr__(self):
        return "Title: %s\n" \
               "Division Number: %d\n" \
               "Ayes: %d\n" \
               "Noes %d\n" \
               "Abstained %d\n" \
               "Margin: %d" % (
                   self.title,
                   self.division_number,
                   self.ayes,
                   self.noes,
                   self.abstained,
                   self.margin,
               )


class MPVote:
    def __init__(self, name, party, vote):
        self.name = name
        self.party = party
        self.vote = vote

    def __repr__(self):
        return "%s, %s\nVoted: %s" % (self.name, self.party, self.vote)


def make_commons_division(primary_topic):
    data = {
        'uin': primary_topic['uin'],
        'title': primary_topic['title'],
        'session': primary_topic['session'][0],
        'division_number': primary_topic['divisionNumber'],
        'date': primary_topic['date']['_value'],
        'deferred_vote': primary_topic['DeferredVote'],
        'non_eligible': primary_topic['Noneligiblecount'][0]['_value'],
        'ayes': primary_topic['AyesCount'][0]['_value'],
        'noes': primary_topic['Noesvotecount'][0]['_value'],
        'abstained': primary_topic['AbstainCount'][0]['_value'],
        'suspended': primary_topic['Suspendedorexpelledvotescount'][0]['_value'],
        'did_not_vote': primary_topic['Didnotvotecount'][0]['_value'],
        'error_vote': primary_topic['Errorvotecount'][0]['_value'],
        'margin': primary_topic['Margin'][0]['_value']
    }
    return CommonsDivision(**data)


def make_mp_vote(vote):
    name = vote['memberPrinted']['_value']
    party = vote['memberParty']
    vote_type = re.search(r'(?:#)(\w+?)(?:Vote)', vote['type'])

    return MPVote(name, party, vote_type.group(1))


if __name__ == '__main__':
    data = getData('http://eldaddp.azurewebsites.net/commonsdivisions')
    result = data['result']
    items = result['items']

    for item in items:
        url = item['_about']
        url = re.sub(
            r'http://data\.parliament\.uk/resources/',
            'http://eldaddp.azurewebsites.net/commonsdivisions/id/',
            url
        )
        data = getData(url)
        result = data['result']
        primary_topic = result['primaryTopic']
        division = make_commons_division(primary_topic)
        print(division)
        votes = primary_topic['vote']
        mps = []
        for vote in votes:
            mp_vote = make_mp_vote(vote)
            print(mp_vote)
