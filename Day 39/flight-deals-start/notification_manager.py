from twilio.rest import Client

# ACCOUNT_SID = 
# AUTH_TOKEN = 


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_sms(self, info):
        text = f"Low price alert! Only £{info['price']} to fly from {info['city_from']}-{info['iata_from']} to {info['city_to']}-{info['iata_to']}, from {info['date_out']} to {info['date_return']}."
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=text,
            from_='+17655629670',
            to='+48691029592',
        )

        print(message.status)
