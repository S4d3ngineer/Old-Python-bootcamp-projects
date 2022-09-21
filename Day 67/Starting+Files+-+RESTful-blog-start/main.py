import datetime
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])  # form does not accept "PUT" and "PATCH" like API requests
def edit_post(post_id):
    post_to_edit = BlogPost.query.get(post_id)
    # populating form with post's data so user can edit it
    edit_post_form = CreatePostForm(
        title=post_to_edit.title,
        subtitle=post_to_edit.subtitle,
        body=post_to_edit.body,
        author=post_to_edit.author,
        img_url=post_to_edit.img_url,
    )
    # putting data posted via wtform into database
    if edit_post_form.validate_on_submit():
        # notice that every column in the table has to be accessed separately to put all the data
        post_to_edit.title = request.form["title"]
        post_to_edit.subtitle = request.form["subtitle"]
        # using original post date
        post_to_edit.date = post_to_edit.date
        post_to_edit.body = request.form["body"]
        post_to_edit.author = request.form["author"]
        post_to_edit.img_url = request.form["img_url"]
        db.session.commit()
        return redirect(url_for("show_post", index=post_id))
    return render_template("make-post.html", form=edit_post_form, heading="Edit Post")


@app.route("/new-post", methods=["GET", "POST"])
def add_post():
    add_post_form = CreatePostForm()
    if add_post_form.validate_on_submit():
        post_date = datetime.datetime.now()
        formatted_date = post_date.strftime("%B %d, %Y")
        new_post = BlogPost(
            title=request.form["title"],
            subtitle=request.form["subtitle"],
            date=formatted_date,
            body=request.form["body"],
            author=request.form["author"],
            img_url=request.form["img_url"],
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=add_post_form, heading="New Post")


@app.route("/delete/<post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(debug=True)
