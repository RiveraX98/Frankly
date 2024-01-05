from models import db, User
from app import app

db.session.rollback()
db.drop_all()
db.create_all()


test1 = User(first_name="Xavier", last_name='Rivera', email = "river@gmail.com", username="kingriv", password="password")




db.session.add(test1)
db.session.commit()