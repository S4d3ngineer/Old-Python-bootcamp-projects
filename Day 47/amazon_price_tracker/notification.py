import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MY_MAIL = 
# PASSWORD = 
# RECEIVER = 


class Notification:

    def send(self, price, name, threshold, url):

        subject = "Price of the product you are observing have dropped!"
        content = f"Price of {name} has dropped under {threshold} and now is only ${price}!\n{url}"

        msg = MIMEMultipart()
        msg['From'] = MY_MAIL
        msg['To'] = RECEIVER
        msg['Subject'] = subject
        body = MIMEText(_text=content, _subtype='plain')
        msg.attach(body)

        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()  # initiating Transport Layer Securit
            connection.login(user=MY_MAIL, password=PASSWORD)
            connection.send_message(msg, from_addr=MY_MAIL, to_addrs=RECEIVER)
