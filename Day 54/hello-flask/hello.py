from flask import Flask


def make_bold(funct):
    def wrapper():
        return f"<b>{funct()}</b>"
    return wrapper  # it means that we return reference to the function (we did not put in parentheses)


def make_emphasis(funct):
    def wrapper():
        return f"<em>{funct()}</em>"
    return wrapper


def make_underlined(funct):
    def wrapper():
        return f"<u>{funct()}</u>"
    return wrapper


app = Flask(__name__)


@app.route("/")
@make_bold
@make_emphasis
@make_underlined
def hello_world():
    return "<p align='center'>Hello, World!</p>"


@app.route("/bye")
def bye():
    return "<p>Bye!</p>"


@app.route("/username/<name>")
def hello_user(name):
    return f"<p>Hello {name}!"


if __name__ == "__main__":
    app.run(debug=True)  # changes are reflected after saving a file
