from flask import Flask, render_template, url_for, request

import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MY_MAIL = 
# PASSWORD = 
# RECEIVER = 

NPOINT_ENDPOINT = 'https://api.npoint.io/c790b4d5cab58020d391'

# getting data for blog posts from API
with requests.get(NPOINT_ENDPOINT) as r:
    blog_data = r.json()

app = Flask(__name__)


# defining send_mail function
def send_mail(subj, cont):
    subject = subj
    content = cont
    msg = MIMEMultipart()
    msg['From'] = MY_MAIL
    msg['To'] = RECEIVER
    msg['Subject'] = subject
    body = MIMEText(_text=content, _subtype='plain')
    msg.attach(body)
    with smtplib.SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()  # initiating Transport Layer Security
        connection.login(user=MY_MAIL, password=PASSWORD)
        connection.send_message(msg, from_addr=MY_MAIL, to_addrs=RECEIVER)


@app.route('/')
def home():
    return render_template('index.html', data=blog_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_mail(subj="test", cont=f"Text: {data['name']}\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage: {data['message']}")
    return render_template('contact.html')


@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    post = blog_data[blog_id - 1]
    return render_template('post.html', data=post)  # you can input parameters into html via this method


if __name__ == '__main__':
    app.run(debug=True)
