from twilio.rest import Client
import smtplib
from datetime import date, timedelta

# ACCOUNT_SID =
# AUTH_TOKEN = 
# data for smtp
# MY_MAIL = 
# PASSWORD =
# RECEIVER =


class NotificationManager:
    def __init__(self):
        self.tomorrow = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.today_plus_6m = (date.today() + timedelta(days=183)).strftime("%d/%m/%Y")

    # This class is responsible for sending notifications with the deal flight details.
    def send_sms(self, info):
        text = f"Low price alert! Only £{info['price']} to fly from {info['city_from']}-{info['iata_from']}" \
               f" to {info['city_to']}-{info['iata_to']}, from {info['date_out']} to {info['date_return']}."
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # backslash is splitting code into two lines
        message = client.messages \
            .create(
            body=text,
            from_='+17655629670',
            to='+48691029592',
        )

        print(message.status)

    def send_email(self, info):
        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_MAIL,
                                to_addrs=RECEIVER,
                                msg=f"Subject:New Low Price Flight!\n\nLow price alert! Only {'£'.encode('utf-8')}"
                                    f" {info['price']} to fly from {info['city_from']}-"
                                    f"{info['iata_from']} to {info['city_to']}-{info['iata_to']}, from "
                                    f"{info['date_out']} to {info['date_return']}."
                                    f"https://www.google.com/flights?hl=en#flt={info['iata_from']}.{info['iata_to']}."
                                    f"{self.tomorrow}*{info['iata_to']}.{info['iata_from']}.{self.today_plus_6m}"
                                )

    def send_alt_email(self, info):
        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_MAIL,
                                to_addrs=RECEIVER,
                                msg=f"Subject:New Low Price Flight!\n\nLow price alert! Only {'£'.encode('utf-8')}"
                                    f" {info['price']} to fly from {info['city_from']}-"
                                    f"{info['iata_from']} to {info['city_to']}-{info['iata_to']}, from "
                                    f"{info['date_out']} to {info['alternate_return']}.\n\nFlight has"
                                    f" {info['max_stepovers']} stepover via {info['via_city']}.\n\n"
                                    f"https://www.google.com/flights?hl=en#flt={info['iata_from']}.{info['iata_to']}."
                                    f"{self.tomorrow}*{info['iata_to']}.{info['iata_from']}.{self.today_plus_6m}"
                                )
