from turtle import Turtle
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.hideturtle()
        self.color('black')
        self.goto(-200, 240)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(arg=f"Level: {self.score}", align='center', font=('Courier', 18, 'normal'))

    def next_level(self):
        self.score += 1
        self.update_score()

    def reset_level(self):
        self.score = 0
        self.update_score()
