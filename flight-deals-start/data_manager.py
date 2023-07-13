import requests, auth
from pprint import pprint
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self) -> None:
        self.endpoint = auth.SHEETY_ENDPOINT

    def get_data(self):
        response = requests.get(url=self.endpoint)
        response.raise_for_status()
        return response.json()['prices']

    def post_data(self, row_id, data):
        response = requests.put(url=f"{self.endpoint}/{row_id}", json=data)
        response.raise_for_status()