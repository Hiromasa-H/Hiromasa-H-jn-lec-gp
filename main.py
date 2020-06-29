from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #disable warnings
app.permanent_session_lifetime = timedelta(minutes = 15)

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id",db.Integer,primary_key = True)
    name = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(100),unique=True)

    def __init__(self,name,email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = Users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user,"") #email is blank for now
            db.session.add(usr)
            db.session.commit()

        flash(f"Login successful","info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You are already logged in","info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods = ["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", user = user, email = email)
    else:
        flash("You are not logged in yet","info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"you have been logged out, {user}!","info")#warning, info, error
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values = Users.query.all())

#run app
if __name__ == "__main__":
    db.create_all() #create db
    app.run(debug = True) #debug = True is for debugging. 