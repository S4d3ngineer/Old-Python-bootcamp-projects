import requests
from datetime import date, timedelta
from pprint import pprint

TEQUILA_API_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
# TEQUILA_API_KEY = 

CITY_FROM = "LON"

tomorrow = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
today_plus_6m = (date.today() + timedelta(days=183)).strftime("%d/%m/%Y")
header = {
    "apikey": TEQUILA_API_KEY,
}

parameters = {
                "fly_from": CITY_FROM,
                "fly_to": "BER",
                "date_from ": tomorrow,
                "date_to": today_plus_6m,
                "curr": "GBP",
                "flight_type": "round",
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "max_stopovers": 0,
            }

with requests.get(TEQUILA_API_SEARCH_ENDPOINT, headers=header, params=parameters) as r:
    input_data = r.json()["data"][0]

dictionary = {
    "price": input_data["price"],
    "city_from": input_data["cityFrom"],
    "iata_from": input_data["flyFrom"],
    "city_to": input_data["cityTo"],
    "iata_to": input_data["flyTo"],
    "date_out": input_data["route"][0]["local_departure"].split("T")[0],
    "date_return": input_data["route"][1]["local_departure"].split("T")[0],
}

print(dictionary)
