from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """connects db to app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f'<User{u.id}{u.username}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    feedback=db.relationship("Feedback", backref="user")

    @classmethod
    def register (cls,fname, lname, email, username, pwd):
        hashed= bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return  cls(first_name=fname,last_name=lname,email=email,username=username,password=hashed_utf8)
    
    @classmethod
    def authenticate(cls,username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False 


class Feedback(db.Model):
    __tablename__ = "feedback"

    def __repr__(self):
        f = self
        return f'<User{f.id}{f.title}{f.content}{f.username}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(30), nullable=False)
    content= db.Column(db.String, nullable=False)
    username= db.Column(db.String, db.ForeignKey("users.username"))
    



   

