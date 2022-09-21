import requests
from twilio.rest import Client

# Provide those
# ACCOUNT_SID = 
# AUTH_TOKEN = 

# OWM_ENDPOINT = 
# api_key = 

parameters = {
    "lat": 51.107883,
    "lon": 17.038538,
    "appid": api_key,
    "exclude": "daily,minutely,current"
}

r = requests.get(OWM_ENDPOINT, params=parameters)
r.raise_for_status()

weather_data = r.json()

will_rain = False
weather_slices = weather_data["hourly"][:12]  # Python slicing operator
for hour_data in weather_slices:
    weather_id = hour_data["weather"][0]["id"]
    if weather_id < 600:
        will_rain = True


def send_sms():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It is going to rain today my friend! Prepare yourself!",
        from_='+17655629670',
        to='+48691029592',
    )

    print(message.status)


if will_rain:
    send_sms()
