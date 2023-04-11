from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waitlist.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)


class WaitlistEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<WaitlistEntry {self.first_name} {self.last_name} {self.email}>"


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")

        # Save the data to the database
        entry = WaitlistEntry(first_name=first_name, last_name=last_name, email=email)
        db.session.add(entry)
        db.session.commit()

        # flash("Thanks for signing up!", "success")
        return redirect(url_for("landing"))
    return render_template("signup.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
