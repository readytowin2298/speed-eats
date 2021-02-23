from app import requests, YELP_KEY, YELP_BASE_URL, Resturaunt, db

r = requests.get(
    YELP_BASE_URL, headers={
        "Authorization" : f"Bearer {YELP_KEY}"
    },
    params={
        "location" : "113 Hancock St Venus texas 76084",
        "limit" : 10,
        "categories" : "food"
    }
)

resturaunt_data = r.json()['businesses']

for resturaunt in resturaunt_data:
    if not Resturaunt.query.filter_by(party_id=1, url=resturaunt['url']).first():

        address = resturaunt['location']['address1']
        if resturaunt['location']['address2']:
            address += resturaunt['location']['address2']
        if resturaunt['location']['address3']:
            address += resturaunt['location']['address3']
        print(address)
        if address:
            new_resturaunt = Resturaunt(
                name=resturaunt['name'],
                address=address,
                city=resturaunt['location']['city'],
                state=resturaunt['location']['state'],
                zip_code=int(resturaunt['location']['zip_code']),
                url=resturaunt['url'],
                party_id=1,
                yelp_id = 
            )
            db.session.add(new_resturaunt)
    else:
        print('Already have it')
db.session.commit()