from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email  # Email requires installing wtforms[email]
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "super-secret-string"


class LoginForm(FlaskForm):
    email = StringField(label="email", validators=[DataRequired(), Email(message='That\'s not a valid email address.')])

    password = PasswordField(label="password", validators=[DataRequired(), Length(min=8, message='Password must have '
                                                                                                 'minimum of 8 '
                                                                                                 'characters.')])
    submit = SubmitField(label="Log In")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # we need this method to validate our form and to use our own validation and not browser's validation
    # we need to put 'novalidate' inside </form> tag
    form.validate_on_submit()
    if form.email.data:
        print(form.email.data)
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
