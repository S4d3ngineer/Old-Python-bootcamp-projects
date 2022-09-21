from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)

        # (this could be done also by dictionary comprehension but this way there we get better structure with comments
        # so everything is more comprehensible)

        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    # As on stranger in the internet said:
    # Apparently this is the quickest way to get a random row from a database that may become large / Scalability
    # Firstly, get the total number of rows in the database
    row_count = Cafe.query.count()
    # Generate a random number for skipping some records
    random_offset = random.randint(0, row_count - 1)
    # Return the first record after skipping random_offset rows
    random_cafe = Cafe.query.offset(random_offset).first()

    return jsonify(
        cafe=random_cafe.to_dict()
    )


@app.route("/all")
def get_all_cafes():
    cafes = Cafe.query.all()
    cafes_list = [cafe.to_dict() for cafe in cafes]

    return jsonify(
        cafes=cafes_list
    )


@app.route("/search")
def search_for_cafe():
    # request.args.get() is going to get arguments value passed via '?parameter=value' either passed into url directly
    # or together when getting trough hyperlink which also passes argument like:
    # <a href="{{ url_for("site", parameter=argument) }}
    loc = request.args.get("loc")
    result = Cafe.query.filter_by(location=loc).first()

    # if result exists (it is not NoneType)
    if result:
        return jsonify(
            cafe=result.to_dict()
        ), 200
    else:
        return jsonify(
            error={"Not Found": "Sorry, we don't have cafe at that location."},
        ), 400


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(
        response={
            "Success": "Successfully added the new cafe.",
        }
    )


# HTTP PUT/PATCH - Update Record
@app.route("/update_price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):

    cafe_to_update = Cafe.query.get(cafe_id)

    if cafe_to_update:
        cafe_to_update.coffee_price = request.args.get("price")
        db.session.commit()
        return jsonify(
            response={
                "Success": "Successfully updated the price.",
            }
        ), 200
    else:
        return jsonify(
            error={"Not Found": "Sorry, you requested id that doesn't exist."},
        ), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):

    cafe_to_delete = Cafe.query.get(cafe_id)

    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(
            response={
                "Success": "Successfully deleted the cafe.",
            }
        ), 200

    else:
        return jsonify(
            error={"Not Found": "Sorry, you requested id that doesn't exist."},
        ), 404


if __name__ == '__main__':
    app.run(debug=True)
