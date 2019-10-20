from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

# Todo: Pull data about MPs from http://data.parliament.uk/membersdataplatform/memberquery.aspx#membershipinfotable
# Note: eg http://data.parliament.uk/membersdataplatform/services/mnis/members/query/commonsmemberbetween=2012-01-01and2012-03-31/
#       Look up data for MPs on any given division day. Compare votes against that list. Add any missing MPs to the database.
from models.member_of_parliament import MemberOfParliament
from orm.orm import session_factory, drop_all


def get_members_for_date(date):
    url = "http://data.parliament.uk/membersdataplatform/services/mnis/members/query"
    url_with_dates = "%s/commonsmemberbetween=%sand%s" % (url, date, date)
    print('Fetching Members On Date: ' + url_with_dates)
    response = requests.get(url_with_dates)
    soup = bs(response.content, "lxml-xml")
    return soup.find_all("Member")


def get_member(id):
    url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/id=' + id
    print('Fetching Member: ' + url)
    response = requests.get(url)
    soup = bs(response.content, "lxml-xml")
    return soup


def make_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except TypeError:
        return None


def make_mp(member_data):
    return MemberOfParliament(
        clerks_id=member_data.get("Clerks_Id"),
        dods_id=member_data.get("Dods_Id"),
        member_id=member_data.get("Member_Id"),
        pims_id=member_data.get("Pims_Id"),
        name=member_data.find("DisplayAs").string,
        full_title=member_data.find("FullTitle").string,
        gender=member_data.find("Gender").string,
        party=member_data.find("Party").string,
        constituency=member_data.find("MemberFrom").string,
        date_of_birth=make_date(member_data.find("DateOfBirth").string),
        date_of_death=make_date(member_data.find("DateOfDeath").string),
        member_since=make_date(member_data.find("HouseStartDate").string),
        end_date=make_date(member_data.find("HouseEndDate").string),
        start_date=make_date(member_data.find("StartDate").string)
    )


def create_mps_for_date(date, session=None):
    session = session or session_factory()
    members = get_members_for_date(date.strftime("%Y-%m-%d"))
    mps = []
    for member in members:
        mp = create_mp(member, session)
        mps.append(mp)
    session.commit()

    return mps


def create_mp(member_data, session=None):
    session = session or session_factory()
    query = session \
        .query(MemberOfParliament) \
        .filter(
        MemberOfParliament.member_id == member_data.get("Member_Id"),
    )
    mp = query.one_or_none()
    if not mp:
        mp = make_mp(member_data)
        session.add(mp)

    return mp


if __name__ == "__main__":
    drop_all()
    session = session_factory()
    create_mps_for_date(datetime(2019, 2, 1), session)
