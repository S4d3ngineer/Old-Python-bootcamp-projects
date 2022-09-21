from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

# TMDP_API_KEY = 
TMDP_API_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDP_API_URL = "https://api.themovipip install Flask-SQLAlchemyedb.org/3/movie/"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250))

    def __repr__(self):
        return f'<Movie {self.title}>'


db.create_all()

# new_movie = Movies(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


class EditForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AddForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/")
def home():
    all_movies = Movies.query.order_by(Movies.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    movie_id = request.args.get("id")
    movie_to_update = Movies.query.get(movie_id)
    edit_form = EditForm()
    # if we want validation done through wtforms and not client-side validation (via browser) we need to set
    # novalidate=True inside a form and validate_on_submit() needs to be used inside 'if' statement
    if edit_form.validate_on_submit():
        movie_to_update.rating = request.form["rating"]
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form, movie=movie_to_update)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()

    if add_form.validate_on_submit():
        with requests.get(TMDP_API_SEARCH_URL, params={'api_key': TMDP_API_KEY, 'query': request.form['title']}) as r:
            response = r.json()["results"]
        print(response)
        return render_template('select.html', movies=response)

    return render_template("add.html", form=add_form)


@app.route("/find")
def find():
    movie_id = request.args.get("id")
    with requests.get(f"{TMDP_API_URL}/{movie_id}", params={"api_key": TMDP_API_KEY}) as r:
        result = r.json()
    new_movie = Movies(
        title=result["title"],
        img_url=f"{MOVIE_DB_IMAGE_URL}{result['poster_path']}",
        year=int(result["release_date"][0:4]),
        description=result["overview"],
    )
    db.session.add(new_movie)
    db.session.commit()
    added_movie = Movies.query.filter_by(title=result["title"]).first()
    return redirect(url_for("edit", id=added_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
