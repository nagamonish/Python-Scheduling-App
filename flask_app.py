from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_migrate import Migrate

##Connects to flask
app = Flask(__name__)
app.config["DEBUG"] = True

##Sets up database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",      #Username, Password, Hostname, and Database name will be shown only to contributors
    hostname="",
    databasename="",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

##Connects database
db = SQLAlchemy(app)
##Allows migrations
migrate = Migrate(app, db)

##Sets up the login system
app.secret_key = "" #Secret key will be shown only to contributors
login_manager = LoginManager()
login_manager.init_app(app)

##Sets up a class for login manager, MUST INCLUDE DB MODEL TO ADD TO DATABASE
class User(UserMixin, db.Model):

    __tablename__ = "users"
    ##Database columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

##Sample database for users


##Gives unique id to users, and QUERY THE USERS TABLE IN THE DATABASE
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

##Makes a model in sql(Basically a column)
class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    ##THIS ADDS A NEW COLUMN BOIIIIIII HERE
    posted = db.Column(db.DateTime, default=datetime.now)

    ## FINDS THE COMMENTER ID AND NAME FROM THE DATABASE, commenter id is database id, commenter is the username
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

##Routes app to main page, GET view data, and POST sends data
@app.route("/comments", methods=["GET", "POST"])
def index():
    ##Gets the data and updates comments using what was in the comment section in html
    if request.method == "GET":
        ##THIS IS WHERE IT EXTRACTS DATA FROM DATABASE (QUERY), timestamp just looks at the date
       return render_template("main_page.html", comments=Comment.query.all())
    ##IF USER IS NOT LOGGED IN IT REDIRECTS YOU TO INDEX so you cant post something
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    ##Else because method must be POST and SENDS the DATA to DATABASE
    ##COMMENT VARIABLE GETS THE CONTENTS OF THE COMMENT AND THE COMMENTER ID
    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

##Routes to main page## ADD THE CODE FOR THE COMMENT PAGE
@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("testdashboard.html")

@app.route("/test")
def dash():
    return render_template("new_main.html")

@app.route("/register/", methods=["GET", "POST"])
def register():
    ##If user is authenticated it redirects to main page, no need for register
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    ##Just viewing the register page
    if request.method == "GET":
         return render_template("register.html")



    ##Work right here
    user = request.form["username"]
    passcode = request.form["password"]
    admin = User(username=user, password_hash=generate_password_hash(passcode))
    db.session.add(admin)

    # user = load_user(request.form["username"])
    # passcode = user.check_password(request.form["password"])
    # admin = User(username="admin", password_hash=generate_password_hash("new-secret"))
    # db.sessio.add(admin)
    db.session.commit()
    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    ##User is just trying view data and login page shows up
    if request.method == "GET":
        return render_template("login_page2.html", error=False)
    ##If user isn't admin or password isnt correct, it shows login page again with error being true
    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page2.html", error=True)
    ##If password is incorrect, login page again with error being true
    if not user.check_password(request.form["password"]):
        return render_template("login_page2.html", error=True)
    ##Everything is correct and index is returned
    login_user(user)
    return redirect(url_for('main'))

##Logout
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/about")
def about():
    return render_template("About-us.html")
