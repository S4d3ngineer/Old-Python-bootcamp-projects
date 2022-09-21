from flask import Flask, render_template
import datetime
import requests

YOUR_NAME = 'Adam'
AGIFY_API_URL = 'https://api.agify.io/?name='
GENDERIZE_API_URL = 'https://api.genderize.io?name='
NPOINT_API_URL = 'https://api.npoint.io/c790b4d5cab58020d391'

app = Flask(__name__)


@app.route('/')
def home():
    current_year = datetime.datetime.now().year
    return render_template('index.html', year=current_year, name=YOUR_NAME)


@app.route('/guess/<name>')
def guess(name):
    current_year = datetime.datetime.now().year
    with requests.get(f"{AGIFY_API_URL}{name}") as r:
        age_data = r.json()
        age = age_data["age"]
    with requests.get(f"{GENDERIZE_API_URL}{name}") as r:
        gender_data = r.json()
        gender = gender_data["gender"]
    return render_template('guess.html', year=current_year, name=YOUR_NAME, some_name=name, gender=gender, age=age)


@app.route('/blog')
def blog():
    with requests.get(NPOINT_API_URL) as r:
        all_posts = r.json()
    return render_template('blog.html', posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)
