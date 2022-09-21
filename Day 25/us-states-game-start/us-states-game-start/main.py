from turtle import Screen, Turtle
import pandas

score = 0
guessed_states = []
screen = Screen()
states_map = Turtle()
screen.title('U.S. States Game')
screen.addshape('blank_states_img.gif')
states_map.shape('blank_states_img.gif')

# jimmy - the turtle which writes state names on the map
jimmy = Turtle()
jimmy.penup()
jimmy.hideturtle()


def write_name(xy):
    jimmy.goto(xy)
    jimmy.write(arg=f'{guess}', font=('Arial', 8, 'normal'), align='center')


# create list of states
states_file = pandas.read_csv('50_states.csv')
states_list = states_file.state.to_list()


def make_guess():
    answer = screen.textinput(f"{score}/{len(states_list)} States Correct", "Enter the state's name below").title()
    return answer


def check_coordinates(guess):
    guessed_row = states_file[states_file.state == guess]
    x = int(guessed_row.x)
    y = int(guessed_row.y)
    xy = (x, y)
    return xy


game_is_on = True
while game_is_on:
    guess = make_guess()
    if score == len(states_list):
        game_is_on = False

    if guess == "Exit":
        break

    # check if guess is in list of states
    for state in states_list:
        if guess == state:

            # if guess is correct write it on the map and update score
            score += 1

            # check state's coordinates
            write_name(check_coordinates(guess))

            # append guessed state to list
            guessed_states.append(guess)

# states_to_learn
# for state in states_list:
#     if state not in guessed_states:
#         missing_list.append(state)
missing_list = [state for state in states_list if state not in guessed_states]
missing_states = pandas.DataFrame(missing_list)
missing_states.to_csv('missing_states.csv')
# screen.mainloop()

