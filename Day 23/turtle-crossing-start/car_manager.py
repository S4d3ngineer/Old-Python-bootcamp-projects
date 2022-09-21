from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.cars = []
        self.move_distance = STARTING_MOVE_DISTANCE

    def generate_car(self):
        new_car = Turtle(shape='square')
        new_car.penup()
        new_car.shapesize(stretch_wid=1, stretch_len=2)
        random_color = random.choice(COLORS)
        new_car.color(random_color)
        random_y = random.randint(-250, 250)
        new_car.goto(300, random_y)
        self.cars.append(new_car)

    def move(self):
        for car in self.cars:
            car.bk(self.move_distance)

    def speed_up(self):
        self.move_distance += MOVE_INCREMENT

    def reset_speed(self):
        self.move_distance = STARTING_MOVE_DISTANCE
