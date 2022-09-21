class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.dictionary = {}

    def process_data(self, input_data):
        """ Making dictionary out of searched flight data."""
        self.dictionary = {
            "price": input_data["price"],
            "city_from": input_data["cityFrom"],
            "iata_from": input_data["flyFrom"],
            "city_to": input_data["cityTo"],
            "iata_to": input_data["flyTo"],
            "date_out": input_data["route"][0]["local_departure"].split("T")[0],
            "date_return": input_data["route"][1]["local_departure"].split("T")[0],
            "alternate_return": "",  # with stepover
            "max_stepovers": "1",
            "via_city": input_data["route"][0]["cityTo"],
        }
        return self.dictionary
