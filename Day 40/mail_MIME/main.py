# Sending email with an attachment

import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# MY_MAIL = 
# PASSWORD = 
# RECEIVER =   # to_addr can be a list and send_message command can accept it

subject = "Test"
content = "Sample text. £"

msg = MIMEMultipart()
msg['From'] = MY_MAIL
msg['To'] = RECEIVER
msg['Subject'] = subject
body = MIMEText(_text=content, _subtype='plain')
msg.attach(body)  # attaching body to the message

# Reading text file to be attached into memory and attaching it to my message as MIMEAplication
filename = 'attachment.txt'
with open(file=filename, mode='r') as f:
    part = MIMEApplication(_data=f.read(), Name=basename(filename))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
msg.attach(part)

# email package is for managing email messages. It is not designed for sending them so in order to do this we are
# using smtplib package
with smtplib.SMTP(host="smtp.gmail.com") as connection:
    connection.starttls()  # initiating Transport Layer Security
    connection.login(user=MY_MAIL, password=PASSWORD)
    connection.send_message(msg, from_addr=MY_MAIL, to_addrs=RECEIVER)

# in order to send multiple attachments one can use loop. Just like in the example below
# filenames = ['test1.txt', 'test2.txt', 'test3.txt']
# for filename in filenames:
#     with open(filename, 'r') as f:
#         part = MIMEApplication(f.read(), Name=basename(filename))
#         part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
#     msg.attach(part)
