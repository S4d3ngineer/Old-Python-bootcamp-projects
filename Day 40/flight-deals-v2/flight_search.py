import requests
from pprint import pprint
from datetime import date, timedelta
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager

TEQUILA_API_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_API_LOCATION_QUERY_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
# TEQUILA_API_KEY = 


class FlightSearch:

    # This class is responsible for talking to the Flight Search API.
    def __init__(self):

        self.tomorrow = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.today_plus_6m = (date.today() + timedelta(days=183)).strftime("%d/%m/%Y")
        self.header = {
            "apikey": TEQUILA_API_KEY,
        }

    def search(self, from_city):

        manager = DataManager()
        data = manager.get_data()

        flight_data = FlightData()

        notification = NotificationManager()

        for city in data:  # for every row in Google Sheets
            parameters = {  # setting parameters for search endpoint
                "fly_from": from_city,
                "fly_to": city["iataCode"],
                "date_from ": self.tomorrow,
                "date_to": self.today_plus_6m,
                "curr": "GBP",
                "flight_type": "round",
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "max_stopovers": 0,
            }
            try:  # try getting cheap flight data according to parameters
                with requests.get(TEQUILA_API_SEARCH_ENDPOINT, headers=self.header, params=parameters) as r:
                    result = r.json()["data"][0]
            except IndexError:  # except there are no flights meeting given criteria
                try:
                    parameters["max_stopovers"] = 2
                    with requests.get(TEQUILA_API_SEARCH_ENDPOINT, headers=self.header, params=parameters) as r:
                        result = r.json()["data"][0]
                    if result["price"] < city["lowestPrice"]:  # if price is lower than recorded in Google Sheets
                        processed_data = flight_data.process_data(input_data=result)
                        processed_data["alternate_return"] = result["route"][3]["local_departure"].split("T")[0]  # dictionary from result data
                        notification.send_alt_email(info=processed_data)
                except IndexError:
                    print(f"Sorry. No flights have been found for {city['iataCode']}.")
                    continue
                else:
                    pprint(result)
            else:
                if result["price"] < city["lowestPrice"]:  # if price is lower than recorded in Google Sheets
                    processed_data = flight_data.process_data(input_data=result)  # dictionary from result data
                    notification.send_email(info=processed_data)


    def get_dest_codes(self, city):
        """ Getting IATA codes using city names """
        parameters = {
            "term": city,
            "location_types": "city",
        }

        with requests.get(TEQUILA_API_LOCATION_QUERY_ENDPOINT, headers=self.header, params=parameters) as r:
            r.raise_for_status()
            result = r.json()
            code = result["locations"][0]["code"]
        return code
