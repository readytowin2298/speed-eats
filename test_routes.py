from app import app, db, User, Party, Resturaunt, Vote
from flask import session
from unittest import TestCase


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
        print("inside setup")

        party = Party.create(address="12345 South Fwy",
                city="Cross Timber",
                state="Texas",
                zip_code=76028,
                leader_id=user1.id,
                name="Valentine's day dinner")
        db.session.add(party)
        db.session.commit()
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
        self.assertIn(us[0], ps[0].members)
        self.assertIn(us[1], ps[0].members)
        self.assertEqual(User.query.filter_by(email="test@test.com").first(), ps[0].leader)
        

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

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