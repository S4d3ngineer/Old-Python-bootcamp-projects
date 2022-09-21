import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = sqlite3.connect("books-collection.db")
#
# cursor = db.cursor()

# cursor.execute(
#     "CREATE TABLE books ("
#     "id INTEGER PRIMARY KEY,"
#     "title varchar(250) NOT NULL UNIQUE,"
#     "author varchar(250) NOT NULL,"
#     "rating FLOAT NOT NULL)"
# )

# cursor.execute(
#     "INSERT INTO books VALUES("
#     "1, 'Harry Potter',"
#     "'J. K. Rowling',"
#     "'9.3')"
# )
# db.commit()

app = Flask(__name__)
# Creating database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# Silencing the depreciation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating SQLAlchemy object by passing it Flask application
db = SQLAlchemy(app)


# Creating table using Model class
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.String(250), unique=False, nullable=False)

    # after reading all the records and printing result f'<ClassName {self.id}>' is going to be printed by default
    # in the line of code below we can change it to output value of another attribute
    def __repr__(self):
        return f'<Book {self.title}>'


# db.create_all()
#
new_book = Book(title='1984', author='M. Orwell', rating=6.9)
db.session.add(new_book)
db.session.commit()

all_books = db.session.query(Book).all()
print(all_books)
