from unittest import TestCase
from app import app
from models import User,Feedback, db, bcrypt



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Test_feedback'
app.config['SQLALCHEMY_ECHO'] = False
app.config["WTF_CSRF_ENABLED"]=False
app.config['TESTING'] = True
db.drop_all()
db.create_all()


class UsersTest(TestCase):

    def setUp(self):
        
        Feedback.query.delete()
        User.query.delete()
        user = User(first_name="John", last_name="Doe", email="Testemail@test.com", username="JohnDoe98", password=bcrypt.generate_password_hash("TestPassword"))
        self.user = user

        feedback = Feedback(title="Helllo World", content="Testing post", username="JohnDoe98")
        self.feedback = feedback

     

        db.session.add_all([user, feedback])
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    
        
    def test_handle_registration(self):
        with app.test_client() as client:
            d = {"first_name":"Jane", "last_name":"Doe", "email":"Fake_email@test.com", "username":"JaneDoe78", "password":"TestPassword"}
            resp = client.post("/register", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Welcome </h1>", html)

    def test_handle_login(self):
        with app.test_client() as client:
            
            data={"username":"JohnDoe98", "password": "TestPassword"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h5>Users Feedback:</h5>", html)
            self.assertIn(f"<p>{self.feedback.title}</p>",html)