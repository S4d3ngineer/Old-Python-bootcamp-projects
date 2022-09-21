from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECKMARK = '✔'
timer = None

reps = 0
checkmarks = ''


# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global checkmarks
    global reps
    window.after_cancel(timer)
    label.config(text='Timer', fg='GREEN')
    canvas.itemconfig(timer_text, text="25:00")
    checkmarks = ''
    checkmarks_labels.config(text=checkmarks)
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1
    if reps % 8 == 0:
        time = LONG_BREAK_MIN
        label.config(text=f'Break', fg=RED)
    elif reps % 2 == 0:
        time = SHORT_BREAK_MIN
        label.config(text=f'Break', fg=PINK)
    else:
        time = WORK_MIN
        label.config(text=f'Work', fg=GREEN)
    count_down(time * 60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(time):
    global reps
    global checkmarks
    global timer
    minutes = math.floor(time / 60)
    seconds = time % 60
    if seconds < 10:
        seconds = '0' + str(seconds)
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if time > 0:
        # TODO change 10 to 1000
        timer = window.after(10, count_down, time - 1)
    else:
        if reps % 2 == 1:
            checkmarks += CHECKMARK
            checkmarks_labels.config(text=checkmarks)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')
window.config(padx=100, pady=100, bg=YELLOW)

label = Label(text='Timer', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 44, 'bold'))
label.grid(column=1, row=0)

canvas = Canvas(width=202, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(102, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text=f'{WORK_MIN}:00', fill='white', font=(FONT_NAME, 30, 'bold'))
canvas.grid(column=1, row=1)

start_button = Button(text='Start', command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text='Reset', command=reset_timer)
reset_button.grid(column=2, row=2)

checkmarks_labels = Label(text=checkmarks, bg=YELLOW, fg=GREEN)
checkmarks_labels.grid(column=1, row=3)

window.mainloop()
