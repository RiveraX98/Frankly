import os
from flask import Flask, render_template, jsonify, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegistrationForm, loginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///feedback' ))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "ihavesecret321")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route("/")
def show_homepage():
    feedback = Feedback.query.all()
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return render_template("homepage.html", posts=feedback, user=user)
   
    flash("Must be logged in", "danger")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def handle_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.register(first_name, last_name, email, username, password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken, Please try again")
            return render_template("registration.html", form=form)

        session["user_id"] = user.id
        flash("Account created successfully", "success")
        return redirect("/")

    return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def handle_login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome, {user.username}!","success")
            session["user_id"] = user.id
            return redirect("/")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    if "user_id" in session:
        user = User.query.filter_by(id=user_id).first()
        feedback = Feedback.query.filter_by(username=user.username).all()
        return render_template("user_details.html", user=user, posts=feedback)
    else:
        return redirect("/login")


@app.route("/logout")
def logout_user():
    session.pop("user_id")
    flash("Logged out successfully", "success")
    return redirect("/login")


@app.route("/users/<int:user_id>/feedback/add", methods=["GET", "POST"])
def add_feedback(user_id):
    form = FeedbackForm()
    user= User.query.filter_by(id=user_id).first()
    url = f"/users/{user_id}/feedback/add"

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=user.username)
        
        db.session.add(feedback)
        db.session.commit()
        flash("Thanks for providing Feedback", "success")
        return redirect(f"/users/{user.id}")

    return render_template("feedback_form.html", form=form, user=user, url=url)


@app.route("/feedback/<feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    post = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=post)
    url = f"/feedback/{feedback_id}/update"
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        user_id= post.user.id
        flash("feedback updated", "success")
        return redirect(f"/users/{user_id}")
    else:
        return render_template("feedback_form.html", form=form, user=post.user, url=url)


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user_id = feedback.user.id
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted successfully", "success")
    return redirect(f"/users/{user_id}")


@app.route("/secret")
def show_secret():
    if "user_id" not in session:
        flash("Login to view this page", "danger")
        return redirect("/login")
    return render_template("secret.html")



