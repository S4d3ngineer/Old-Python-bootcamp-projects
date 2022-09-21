import smtplib
import datetime as dt
import random

MY_MAIL = "bob.universe.destroyer@gmail.com"
PASSWORD = "Oee5NOa#Lo32C&3"
RECEIVER = "bob.builderoftheuniverse@yahoo.com"


def send_mail(text):
    # opening connection using SMTP class from smtplib
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # initiating tls (transport layer security)
        connection.starttls()
        connection.login(user=MY_MAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_MAIL,
                            to_addrs=RECEIVER,
                            msg=f"Subject: Motivational quote\n\n{text}"
                            )


# when you need to get specific parameter from datetime format, such as month, year, minute etc.
# you need to first create datetime object using line below, and then you can get specific parameter from that object,
# using its specific method
now = dt.datetime.now()
weekday = now.weekday()

if weekday == 3:

    with open("quotes.txt") as quotes_file:
        quotes_list = quotes_file.readlines()
    quote = random.choice(quotes_list)

    send_mail(text=quote)
