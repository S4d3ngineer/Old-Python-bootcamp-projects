import requests

SHEETY_ENDPOINT = "https://api.sheety.co/f65effd2e7e2d8e7ed4732f0df280f70/flightDeals/prices"
# BEARER_TOKEN = 


class DataManager:

    # this class is responsible for talking to the Google Sheet.
    def __init__(self):

        self.sheety_header = {
            "Authorization": "Bearer ZvH3dzja8&u%(0*",
        }
        self.data = {}

    def update_dest_codes(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            with requests.put(f"{SHEETY_ENDPOINT}/{city['id']}", headers=self.sheety_header, json=new_data) as r:
                print(r.text)

    def get_data(self):
        # getting data contained inside Google Docs sheet and storing it inside data attribute
        with requests.get(SHEETY_ENDPOINT, headers=self.sheety_header) as r:
            result = r.json()
        self.data = result["prices"]

        # checking if data contains IATA codes and updating data with codes corresponding to the cities
        should_update = False
        for data in self.data:
            if data["iataCode"] == "":
                should_update = True
                from flight_search import FlightSearch
                flight_search = FlightSearch()
                new_code = flight_search.get_dest_codes(data["city"])
                data["iataCode"] = new_code
        if should_update:
            self.update_dest_codes()
        return self.data
