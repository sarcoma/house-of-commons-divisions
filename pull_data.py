from commons_divisions.pull_commons_divisions import pull_commons_divisions

next_url = 'http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=0'
while True:
    next_url = pull_commons_divisions(next_url)
    if not next_url:
        break
