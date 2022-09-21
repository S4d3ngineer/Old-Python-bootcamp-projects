import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.listen()

player = Player()
car = CarManager()
scoreboard = Scoreboard()

counter = 0

screen.onkey(player.move_up, 'w')
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    counter += 1
    if counter % 6 == 0:
        car.generate_car()
        counter = 0
    car.move()
    for single_car in car.cars:
        if single_car.distance(player) < 20:
            player.reset_position()
            car.reset_speed()
            scoreboard.reset_level()
    if player.ycor() > 300:
        player.reset_position()
        car.speed_up()
        scoreboard.next_level()
    screen.update()

screen.exitonclick()
