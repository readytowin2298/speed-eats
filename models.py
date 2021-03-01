from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from secret import GEO_KEY, YELP_KEY, YELP_CLIENT_ID
import requests
bcrypt = Bcrypt()
db = SQLAlchemy()

YELP_BASE_URL = "https://api.yelp.com/v3/businesses/search"


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for all Users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    email = db.Column(db.String(50),
                unique=True,
                nullable=False)
    password = db.Column(db.Text,
                nullable=False)
    name = db.Column(db.String(20),
                nullable=False)
    parties = db.relationship('Party',
                secondary='party_members',
                backref='members')
    @classmethod
    def create(cls, email, password, name):
        
        if User.query.filter_by(email=email).first():
            return 'Email already in use'
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')
        u = User(email=email, password=hashed_pw, name=name)
        db.session.add(u)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return None
        return u
    @classmethod
    def authenticate(cls, email, password):
        u = User.query.filter_by(email=email).first()
        if u:
            pw_hash = u.password
            if bcrypt.check_password_hash(pw_hash, password):
                return u
        return None


class Party(db.Model):
    """Group Users, votes, and resturaunts"""

    __tablename__  = 'parties'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    address = db.Column(db.Text,
                nullable=False)
    city = db.Column(db.Text,
                nullable=False)
    state = db.Column(db.Text,
                nullable=False)
    zip_code = db.Column(db.Integer,
                nullable=False)
    leader_id = db.Column(db.ForeignKey('users.id'),
                nullable=False)
    leader = db.relationship('User', 
                backref='owned_parties')
    name = db.Column(db.Text)

    decided = db.Column(db.Boolean,
                nullable=False,
                default=False)
    decided_resturaunt_id = db.Column(db.Integer,
                nullable=True)
    accepting_members = db.Column(db.Boolean,
                nullable=False,
                default=True)
    @classmethod
    def create(cls, address, city, state, zip_code, leader_id, name):
        """Create party, location data refers to 
        central poi, must have a leader"""
        try:
            zip_code = int(zip_code)
        except:
            return None
        leader = User.query.get_or_404(leader_id)
        p = Party(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            leader_id=leader.id,
            name=name
        )
        db.session.add(p)
        db.session.commit()
        added_to_party = p.add_member(leader_id)
        if not added_to_party:
            return "Couldn't create that party"
        resturaunts = Resturaunt.get_resturaunts(party_id=p.id)
        if not resturaunts:
            return "Couldn't find resturaunts near there!"
        return p


    def add_member(self, member_id):
        """Add member to party"""
        if self.accepting_members == False:
            return None
        u = User.query.filter_by(id=member_id)
        if u:
            pm = PartyMember(member_id=member_id, party_id=self.id)
            db.session.add(pm)
            try:
                db.session.commit()
                return u
            except:
                return None
            

    def add_resturaunt(self, name, address, city, state, zip_code, url, yelp_id, image_url):
        """Create resturaunt attached to this party"""
        try:
            zip_code = int(zip_code)
        except:
            return 'Invalid Zip'

        r = Resturaunt(name=name,
            address=address,
            city=city, state=state,
            zip_code=zip_code,
            url=url,
            party_id=self.id,
            yelp_id=yelp_id,
            image_url=image_url)
        db.session.add(r)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return 'Database Error'
        return r

    def count_all_votes(self):
        """Returns a dict with votes counts per resturaunt"""
        votes = self.votes
        if self.done_voting():
            vote_dict = {}
            for resturaunt in self.resturaunts:
                if resturaunt.voted_out == False:
                    vote_dict[resturaunt.id] = 0
            for vote in votes:
                if vote.yay_or_nay:
                    vote_dict[vote.resturaunt_id] += 1
            return vote_dict
        return None
    
    def get_full_address(self):
        """Returns formatted full address from Party"""
        return self.address + ", " + self.city + ", " + self.state + ", " + str(self.zip_code)
    
    def done_voting(self):
        """Determines if enough votes have been cast to pick a winner"""
        curr_resturaunts = Resturaunt.query.filter_by(party_id=self.id, voted_out=False).all()
        votes = Vote.query.filter_by(party_id=self.id).all()
        curr_votes = []
        for vote in votes:
            if vote.resturaunt.voted_out == False:
                curr_votes.append(vote)
        if len(self.members) * len(curr_resturaunts) == len(curr_votes):
            return True
        return False

    
    
    
        

                







class PartyMember(db.Model):
    """Reference of all members 
    attending a party, includes party leader"""

    __tablename__ = 'party_members'

    member_id = db.Column(db.ForeignKey('users.id'),
                primary_key=True)
    party_id = db.Column(db.ForeignKey('parties.id'),
                primary_key=True)

class Resturaunt(db.Model):
    """Possible resturaunts, unique entry 
    for different party id"""

    __tablename__ = 'resturaunts'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    name = db.Column(db.Text,
                nullable=False)
    address = db.Column(db.Text,
                nullable=False)
    city = db.Column(db.Text,
                nullable=False)
    state = db.Column(db.Text,
                nullable=False)
    zip_code = db.Column(db.Integer,
                nullable=False)
    url = db.Column(db.Text,
                nullable=True)
    party_id = db.Column(db.ForeignKey('parties.id'),
                nullable=False)
    voted_out = db.Column(db.Boolean,
                nullable=False,
                default=False)
    party = db.relationship('Party',
                backref='resturaunts')
    yelp_id = db.Column(db.Text,
                nullable=True)
    image_url = db.Column(db.Text,
                nullable=False)
    votes = db.relationship('Vote',
                cascade="delete,all",
                backref='resturaunt')
    
    
    @classmethod
    def get_resturaunts(cls, party_id, count=10):
        party = Party.query.filter_by(id=party_id).first()
        if not party:
            return None
        curr_resturaunts = Resturaunt.query.filter_by(party_id=party.id).all()
        offset = len(curr_resturaunts)
        r = requests.get(
            YELP_BASE_URL, headers={
                "Authorization" : f"Bearer {YELP_KEY}"
            },
            params={
                "location" : party.get_full_address(),
                "limit" : count,
                "categories" : "Resturaunts",
                "offset" : offset
            }
        )
        resturaunt_data = r.json()['businesses']
        resturaunts = []
        for resturaunt in resturaunt_data:
            if not Resturaunt.query.filter_by(party_id=party.id, yelp_id=resturaunt['id']).first():
                address = ""
                if resturaunt['location']['address1']:
                    address += resturaunt['location']['address1']
                if resturaunt['location']['address2']:
                    address += resturaunt['location']['address2']
                if resturaunt['location']['address3']:
                    address += resturaunt['location']['address3']
                if address:
                    new_resturaunt = party.add_resturaunt(
                        name=resturaunt['name'],
                        address=address,
                        city=resturaunt['location']['city'],
                        state=resturaunt['location']['state'],
                        zip_code=int(resturaunt['location']['zip_code']),
                        url=resturaunt['url'],
                        yelp_id=resturaunt['id'],
                        image_url=resturaunt['image_url']
                    )
                    
                    resturaunts.append(new_resturaunt)
                    
        return resturaunts

    def get_full_address(self):
        address = self.address
        address += ', '
        address += self.city
        address += ', '
        address += self.state
        address += ' '
        address += str(self.zip_code)
        return address

    def get_positive_votes(self):
        votes = Vote.query.filter_by(resturaunt_id=self.id, yay_or_nay=True).all()
        return len(votes)
                    


class Vote(db.Model):
    """Record of votes cast, 1 per 
    member/party/resturaunt combo"""

    __tablename__ = 'votes'

    party_id = db.Column(db.ForeignKey('parties.id'),
                primary_key=True)
    member_id = db.Column(db.ForeignKey('users.id'),
                primary_key=True)
    resturaunt_id = db.Column(db.ForeignKey('resturaunts.id'),
                primary_key=True)
    yay_or_nay = db.Column(db.Boolean,
                nullable=True)
    party = db.relationship('Party',
                backref='votes')
    member = db.relationship('User',
                backref='votes')
    # resturaunt = db.relationship('Resturaunt',
    #             cascade='all,delete',
    #             backref='votes')
    
    @classmethod 
    def vote(cls, member, party_id, resturaunt_id, yay):
        """Adds vote to db, takes member object,
        resturaunt id, and yay/nay(boolean)"""
        r = Resturaunt.query.filter_by(id=resturaunt_id).first()
        p = Party.query.filter_by(id=party_id).first()
        already_voted = Vote.query.filter_by(party_id=p.id, member_id=member.id, resturaunt_id=r.id).first()
        if already_voted:
            return 'Already Voted for this resturaunt'
        
        if r and p:
            v = Vote(party_id=party_id,
                member_id=member.id,
                resturaunt_id=resturaunt_id,
                yay_or_nay=yay)
            db.session.add(v)
            try:
                db.session.commit()
                return v
            except:
                return 'Database Error'
        return "Couldn't find resources"
    
    @classmethod
    def get_winners(cls, party_id):
        """Returns a list of every resturaunt that recievd more than half the votes,
        keys are resturaunt ids and values are number of votes"""

        p = Party.query.filter_by(id=party_id).first()
        if p:
            if p.done_voting():
                resturaunts = [resturaunt for resturaunt in p.resturaunts 
                    if resturaunt.voted_out == False] 
                winners = []
                for resturaunt in resturaunts:
                    votes = Vote.query.filter_by(resturaunt_id=resturaunt.id, yay_or_nay=True).all()
                    if len(votes) >= len(p.members)/2:
                        winners.append(resturaunt)
                    else:
                        resturaunt.voted_out = True
                        db.session.add(resturaunt)
                db.session.commit()
                return winners
        return None
                


                

    

    

    
