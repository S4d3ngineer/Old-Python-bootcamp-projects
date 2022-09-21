import requests
from datetime import datetime

SHEETY_ENDPOINT = "https://api.sheety.co/f65effd2e7e2d8e7ed4732f0df280f70/workoutsTracking/workouts"
# BEARER_TOKEN = 

# headers constants for Nutritrionix
APP_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
# APP_ID =
# APP_KEY = 


# params constants for Nutritrionix
GENDER = "male"
WEIGHT_KG = 78
HEIGHT_CM = 188
AGE = 25

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

query = input("Which exercises you did? ")

parameters = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}


# getting results from Nutritrionix
with requests.post(APP_ENDPOINT, headers=headers, json=parameters) as r:
    result = r.json()

# preparing input data for sheety
today = datetime.now()
today_date = today.date().strftime("%d/%m/%Y")
today_time = today.time().strftime("%H:%M:%S")

sheety_header = {"Authorization": "Bearer OeEQ2maV2+3l1Z#A"}

for result in result["exercises"]:
    sheety_jason = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": result["name"].title(),
            "duration": result["duration_min"],
            "calories": result["nf_calories"],
        }
    }

    with requests.post(SHEETY_ENDPOINT, json=sheety_jason, headers=sheety_header) as r:
        print(r.text)
