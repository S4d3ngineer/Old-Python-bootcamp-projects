import requests
from datetime import datetime

# Provide credentials
# USERNAME = 
# TOKEN = 

PIXELA_API = "https://pixe.la/v1/users"

today = datetime.now()
today_formatted = today.strftime("%Y%m%d")

parameters = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(PIXELA_API, json=parameters)
# print(response.text)

GRAPH_ENDPOINT = f"{PIXELA_API}/{USERNAME}/graphs"

graph_config = {
    "id": "graph1",
    "name": "Meditation Record",
    "unit": "commit",
    "type": "int",
    "color": "ajisai",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(GRAPH_ENDPOINT, json=graph_config, headers=headers)
# print(response.text)

post_parameters = {
    "date": "20220129",
    "quantity": "1",
}

response = requests.post(f"{GRAPH_ENDPOINT}/graph1", json=post_parameters, headers=headers)
print(response.text)

put_parameters = {
    "quantity": "0",
}

# response = requests.put(f"{GRAPH_ENDPOINT}/graph1/{today_formatted}", json=put_parameters, headers=headers)
# print(response.text)

response = requests.delete(f"{GRAPH_ENDPOINT}/graph1/{today_formatted}", headers=headers)
print(response.text)
