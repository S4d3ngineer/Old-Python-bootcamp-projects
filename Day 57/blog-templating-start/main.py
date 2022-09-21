from flask import Flask, render_template
import requests

NPOINT_ENDPOINT = 'https://api.npoint.io/c790b4d5cab58020d391'

# getting data for blog posts from API
with requests.get(NPOINT_ENDPOINT) as r:
    blog_data = r.json()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", data=blog_data)


@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    post = blog_data[blog_id - 1]
    return render_template("post.html", data=post)


if __name__ == "__main__":
    app.run(debug=True)
