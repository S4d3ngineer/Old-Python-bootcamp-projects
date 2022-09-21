from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    words_dataframe = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_dataframe = pandas.read_csv("data/french_words.csv")
    words_dictionary = words_dataframe.to_dict(orient="records")
else:
    words_dictionary = words_dataframe.to_dict(orient="records")
current_card = {}


# --------------------------------PICK RANDOM WORD------------------------------------ #
def new_card():
    global current_card, flash_timer
    window.after_cancel(flash_timer)
    current_card = random.choice(words_dictionary)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_content, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=card_front)
    flash_timer = window.after(3000, flash_card)


# --------------------------------PICK RANDOM WORD------------------------------------ #
def remove_card():
    global current_card
    words_dictionary.remove(current_card)
    new_df = pandas.DataFrame.from_dict(words_dictionary)
    new_df.to_csv("data/words_to_learn.csv", index=False)


# --------------------------------PICK RANDOM WORD------------------------------------ #
def flash_card():
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_content, text=current_card["English"], fill='white')
    canvas.itemconfig(card, image=card_back)


# --------------------------------SCREEN SETUP------------------------------------ #
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title('Flashy')

flash_timer = window.after(3000, flash_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
# you should not create images inside functions because when the function ends reference to the image is gone
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
card = canvas.create_image(0, 0, image=card_front, anchor="nw")
card_title = canvas.create_text(400, 150, text="", font=('Ariel', 40, 'italic'))
card_content = canvas.create_text(400, 263, text="", font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=new_card)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0,
                      command=lambda: [new_card(), remove_card()])
right_button.grid(column=1, row=1)

new_card()

window.mainloop()
