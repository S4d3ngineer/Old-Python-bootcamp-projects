from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Creating database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
# Silencing the depreciation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating SQLAlchemy object by passing it Flask application
db = SQLAlchemy(app)


# DataBase object for books
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.String(250), nullable=False)

    # after reading all the records and printing result f'<ClassName {self.id}>' is going to be printed by default
    # in the line of code below, we can change it, to output value of another attribute
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Books(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    # we are getting back book id from edit.html and using it to select book instance to be updated, then change its
    # rating value to one sent via edit form
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    # after accessing site via <a> tag in index.html we get id of the book, then we select it in database and
    # pass book object into edit.html template, so we can get its values inside this template
    # request.args.get('id') gets id value passed into route of the site
    book_id = request.args.get('id')
    print(book_id)
    book_selected = Books.query.get(book_id)
    return render_template('edit.html', book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
