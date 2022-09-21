import datetime as dt
import pandas
import random
import smtplib

MY_MAIL = "bob.universe.destroyer@gmail.com"
PASSWORD = "Oee5NOa#Lo32C&3"

##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv
# done
# 2. Check if today matches a birthday in the birthdays.csv
# creating datetime object
now = dt.datetime.now()
# getting month and day parameters from datetime object
month = now.month
day = now.day
date_tuple = (month, day)

dataframe = pandas.read_csv("birthdays.csv")
dictionary = {(row.month, row.day): row for (index, row) in dataframe.iterrows()}

# 3. If step 2 is true, pick a random letter from letter templates
# and replace the [NAME] with the person's actual name from birthdays.csv
letter_list = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

if date_tuple in dictionary:
    name = dictionary[date_tuple]['name']
    letter = random.choice(letter_list)

    # this line opens file in read mode but under an alias, but it still has not been read
    with open(f"letter_templates/{letter}", "r") as letter_file:
        # now the file has been read and is stored as a string in variable, so we can access it even after closing file
        letter = letter_file.read()

    # text replacement comes out as an output in this case 'letter' is never changed,
    # so we have to store output in a new variable
    # I could also make this line letter = letter.replace(... but let's leave it for now
    new_letter = letter.replace("[NAME]", name)


# 4. Send the letter generated in step 3 to that person's email address.
# opening connection using SMTP class from smtplib
with smtplib.SMTP("smtp.gmail.com") as connection:
    # initiating tls (transport layer security)
    connection.starttls()
    connection.login(user=MY_MAIL, password=PASSWORD)
    connection.sendmail(from_addr=MY_MAIL,
                        to_addrs=dictionary[date_tuple]['email'],
                        msg=f"Subject: Happy Birthday!\n\n{new_letter}"
                        )

# you can automate this code using pythonanywhere.com
# you have to upload every file using the same folders though
