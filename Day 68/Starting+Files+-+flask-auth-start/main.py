from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
user = UserMixin()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form["email"]):
            flash("The email you have entered is already registered. Log in instead!")
            return redirect(url_for('login'))

        else:

            # hashing & salting password
            hashed_and_salted_password = generate_password_hash(
                request.form["password"],
                method="pbkdf2:sha256",
                salt_length=8
            )

            new_user = User(
                email=request.form["email"],
                password=hashed_and_salted_password,
                name=request.form["name"],
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("secrets", name=request.form["name"]))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        found_user = User.query.filter_by(email=email).first()
        if not found_user:
            flash("Invalid email")
        elif not check_password_hash(found_user.password, request.form["password"]):
            flash("Password incorrect")
        else:
            login_user(found_user)
            return redirect(url_for('secrets'))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    user_name = current_user.name
    return render_template("secrets.html", name=user_name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', "files/cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
