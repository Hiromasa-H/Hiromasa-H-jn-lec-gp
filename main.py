from flask import Flask,redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "123"
app.permanent_session_lifetime = timedelta(minutes = 15)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
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

"""
@app.route("/<name>")
def test(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))
"""

#run app
if __name__ == "__main__":
    app.run(debug = True) #debug = True is for debugging. 