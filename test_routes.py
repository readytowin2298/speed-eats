from app import app, db, User, Party, Resturaunt, Vote, PartyForm, UserForm, LoginForm
from unittest import TestCase
import random


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///speed_eats_test'
app.config['WTF_CSRF_ENABLED'] = False
# class TestRoutes(TestCase):

#     # executed prior to each test
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///speed_eats_test'
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()
 
#         # Disable sending emails during unit testing
#         mail.init_app(app)
#         self.assertEqual(app.debug, False)

class TotalTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        db.drop_all()
        db.create_all()

        user1 = User.create(email="test@test.com", name="Johnny Doe", password="testtesttest")
        user2 = User.create(email='test2@test.com', name='Jamie Doe', password='iHaveNotBeenHashed')

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        party = Party.create(address="12345 South Fwy",
                city="Cross Timber",
                state="Texas",
                zip_code=76028,
                leader_id=user1.id,
                name="Valentines day dinner")
        db.session.add(party)
        db.session.commit()
        Resturaunt.get_resturaunts(party_id=party.id)
        self.party=party
        party.add_member(member_id=user2.id)

    
        

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_models(self):
        """Test models created in setup"""
        us = User.query.all()
        ps = Party.query.all()
        rs = Resturaunt.query.all()

        self.assertEqual(len(us), 2)
        self.assertEqual(len(ps), 1)
        self.assertIn(us[0], self.party.members)
        self.assertIn(us[1], self.party.members)
        self.assertEqual(User.query.filter_by(email="test@test.com").first(), self.party.leader)
        

    def test_party_view(self):
        party_name = self.party.name
        party_id = self.party.id
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = '1'
                
            resp = client.get(f"/parties/{party_id}")
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(f"""<h3 class="display-3">""", html)
        self.assertIn(f"Party: {party_name}", html)

    def test_voting(self):
        party_name = self.party.name
        party_id = self.party.id
        leader_name = self.party.leader.name
        for member in self.party.members:
            for resturaunt in self.party.resturaunts:
                vote = True if random.randint(0,1) else False
                new_vote = Vote.vote(member=member,
                            party_id=self.party.id,
                            resturaunt_id=resturaunt.id,
                            yay=vote)
        self.assertTrue(self.party.done_voting())

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = '1'
            resp = client.get(f"/parties/{party_id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

        self.assertIn(f"""<a href="" class="nav-link">{leader_name}</a>""", html)

    def test_create_party(self):
        correct_count = (len(Party.query.all()) + 1)
        leader_id = self.party.leader.id

        with app.app_context():
            form = PartyForm()
            form.name.data = 'Test'
            form.address.data = '3112 E Broad St'
            form.city.data = 'Mansfield'
            form.state.data = 'Texas'
            form.zip_code.data ='76063'
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = leader_id
            resp = client.post('/parties/create', data=form.data)
        self.assertEqual(len(Party.query.all()), correct_count)
        self.assertEqual(resp.status_code, 302)
    
    def test_delete_party(self):
        party_id = self.party.id
        leader_id = self.party.leader.id  

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = leader_id
            resp = client.post(f"/parties/delete/{party_id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

        self.assertEqual(len(Party.query.all()), 0)   
        self.assertIn('Party was successfully deleted', html)    

    def test_login(self):
        email="test@test.com"
        password="testtesttest"
        with app.app_context():
            form = LoginForm()
            form.email.data = email
            form.password.data = password
        with app.test_client() as client:
            resp = client.post(f"/login", data=form.data, follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Johnny Doe", html)

    def test_logout(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = self.party.leader.id
            resp = client.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertIn('Come back soon!', html)

    def test_signup(self):
        email = 'bryan_hale@speedeats.com'
        with app.app_context():
            form = UserForm()
            form.name.data = "Bryan"
            form.password.data = 'supersecurepassword'
            form.email.data = email
        with app.test_client() as client:
            resp = client.post('/signup', data=form.data, follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertTrue(User.query.filter_by(email=email).first())
        self.assertIn('Success! Account created!', html)
        self.assertIn('You have been automatically logged in', html)



    # Through this project I have learned the importance of writing tests as you go