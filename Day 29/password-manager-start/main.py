from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

FONT = ('Arial', 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": username,
        "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title='warning', message="Please don't leave empty fields")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # Reading existing data
                data = json.load(data_file)
                # Updating existing data with new data
                data.update(new_data)

        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            with open('data.json', 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Search error", message="No data file found.")
    else:
        # Here there is no pint in using except method to catch KeyError
        # because it can be done just by 'if' and 'else' statements
        # however we have no option to do this with FileNotFoundError, so we used 'except' above
        if website in data:
            messagebox.showinfo(title=website,
                                message=f"Username: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="Search error", message="No website found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50, bg='white')
window.title('Password Manager')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo = PhotoImage(file='logo.png')
canvas.create_image(0, 0, image=logo, anchor='nw')
canvas.grid(column=1, row=0)

website_label = Label(text='Website:', bg='white', font=FONT)
website_label.grid(column=0, row=1)
website_entry = Entry(width=30)
website_entry.insert(END, string='')
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

username_label = Label(text='Email/Username:', bg='white', font=FONT)
username_label.grid(column=0, row=2)
username_entry = Entry(width=51)
username_entry.insert(0, string='adam.arkuszynski@gmail.com')
username_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text='Password:', bg='white', font=FONT)
password_label.grid(column=0, row=3)
password_entry = Entry(width=30)
password_entry.insert(END, string='')
password_entry.grid(column=1, row=3)
password_button = Button(text='Generate Password', command=generate_password, font=FONT)
password_button.grid(column=2, row=3)

add_button = Button(text='Add', width=39, command=save, font=FONT)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
