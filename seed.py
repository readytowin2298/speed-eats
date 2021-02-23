from models import User, db, Party, Vote
import random

db.drop_all()
db.create_all()

me = User.create(email='test1@test.com', name='david', password='test')
kynsi = User.create(email='test2@test.com', name='kynsi', password='test')
chris = User.create(email='test3@test.com', name='chris', password='test')
tori = User.create(email='test4@test.com', name='tori', password='test')

valentine = Party.create(address="12248 Hunter's Knoll Dr",
    city="Burleson",
    state="Texas",
    zip_code=76028,
    leader_id=me.id,
    name="Valentine's day dinner")

valentine.add_member(kynsi.id)

valentine.add_member(chris.id)

valentine.add_member(tori.id)

for member in valentine.members:
    for resturaunt in valentine.resturaunts:
        vote = True if random.randint(0,1) else False
        Vote.vote(member=member,
                    party_id=valentine.id,
                    resturaunt_id=resturaunt.id,
                    yay=vote)


