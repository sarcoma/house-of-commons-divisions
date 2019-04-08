import requests
from bs4 import BeautifulSoup as bs


# Todo: Pull data about MPs from http://data.parliament.uk/membersdataplatform/memberquery.aspx#membershipinfotable
# Note: eg http://data.parliament.uk/membersdataplatform/services/mnis/members/query/commonsmemberbetween=2012-01-01and2012-03-31/
#       Look up data for MPs on any given division day. Compare votes against that list. Add any missing MPs to the database.

def getMembersForDate(date):
    url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query'
    response = requests.get('%s/commonsmemberbetween=%sand%s' % (url, date, date))
    return bs(response.content, "lxml-xml")


if __name__ == '__main__':
    soup = getMembersForDate('2016-01-01')
    members = soup.find_all('Member')
    print(len(members))
    for member in members:
        print(member)
        print(member.get('Clerks_Id'))
        print(member.get('Dods_Id'))
        print(member.get('Member_Id'))
        print(member.get('Pims_Id'))
        print(member.find('DisplayAs').string)
        print(member.find('FullTitle').string)
        print(member.find('Gender').string)
        print(member.find('Party').string)
        print(member.find('MemberFrom').string)
        print(member.find('DateOfBirth').string)
        print(member.find('DateOfDeath').string)
        print(member.find('HouseStartDate').string)
        print(member.find('HouseEndDate').string)
        print(member.find('StartDate').string)
