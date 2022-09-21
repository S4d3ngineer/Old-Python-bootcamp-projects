import requests
from datetime import datetime
import smtplib
import time

# Provide those
# MY_MAIL = 
# PASSWORD = 
# RECEIVER = 


def send_email():
    with smtplib.SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_MAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_MAIL,
                            to_addrs=RECEIVER,
                            msg=f"Subject: Look at the sky!\n\nThe ISS should be visible above your location"
                                f" if the weather is right!"
                            )


MY_LAT = 51.107883  # Your latitude
MY_LONG = 17.038538  # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT + 5) > iss_latitude > (MY_LAT - 5) and (MY_LONG + 5) > iss_longitude > (MY_LONG - 5):
        return True

# Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_dark_outside():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    current_hour = time_now.hour
    if not sunset > current_hour > sunrise:
        return True


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    time.sleep(60)
    if is_dark_outside() and is_iss_overhead():
        send_email()
