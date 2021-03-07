from app import app, db, User, Party, Resturaunt, Vote, do_login, do_logout
from flask import session
from unittest import TestCase
import random


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///speed_eats_test'

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

class UserViewsTestCase(TestCase):
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


    def test_setUp(self):
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
        with app.test_client() as client:
            resp = client.get(f"/parties/{self.party.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<h3 class="display-3">
                Details for:""", html)
            self.assertIn(f"Party: {self.party.name}", html)

    def test_voting(self):
        for member in self.party.members:
            for resturaunt in self.party.resturaunts:
                vote = True if random.randint(0,1) else False
                new_vote = Vote.vote(member=member,
                            party_id=self.party.id,
                            resturaunt_id=resturaunt.id,
                            yay=vote)
        self.assertTrue(self.party.done_voting())

        with app.test_client() as client:
            do_login(user=self.party.leader)
            resp = client.get(f"/parties/{self.party.id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn(f"""<a href="" class="nav-link">{self.party.leader.name}</a>""", html)
            
        

    # def test_show_user(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/users/{self.id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<title>Blog Master', html)

    # def test_add_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name": "Jane", "last_name": "Doe"}
    #         resp = client.post("/users/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 400)