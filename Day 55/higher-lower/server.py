from flask import Flask
import random

random_number = random.randint(0, 9)
print(random_number)


app = Flask(__name__)


@app.route("/")
def display_guess():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' width=200/>"


@app.route("/<int:number>")
def guessed_number(number):
    if number > random_number:
        return "<h1 style='color: blue'>Your guessed number is too high!</h1>" \
               "<img src='https://i.giphy.com/media/wHB67Zkr63UP7RWJsj/giphy.webp' width=300/>"
    elif number == random_number:
        return "<h1 style='color: green'>Your have guessed the number!</h1>" \
               "<img src='https://i.giphy.com/media/lnlAifQdenMxW/giphy.webp' width=300/>"
    else:
        return "<h1 style='color: brown'>Your guessed number is too low!</h1>" \
               "<img src='https://i.giphy.com/media/li0dswKqIZNpm/giphy.webp' width=300/>"


if __name__ == "__main__":
    app.run(debug=True)


