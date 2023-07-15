import auth, requests, flight_data
import datetime as dt
from dateutil.relativedelta import relativedelta
from pprint import pprint
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self) -> None:
        self.token = auth.TEQUILA_TOKEN
        self.base_endpoint = auth.TEQUILA_BASE_ENDPOINT
        self.headers = {"apikey" : self.token}
        self.flights_found = []

    def give_IATA(self, city):
        params = {
            "term" : city,
        }
        response = requests.get(url=f"{self.base_endpoint}locations/query", params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        IATA_code = data['locations'][0]['code']
        return IATA_code

    def find_flights(self, IATA_from, IATA_to, city_to):
        # tomorrow and 6 months in the future
        # Print the city and the price for all the cities
        # creating a ds of flight_data
        tomorrow = dt.datetime.now() + dt.timedelta(days=1)
        six_months = (tomorrow + relativedelta(months=6)).strftime("%d/%m/%Y")
        tomorrow = tomorrow.strftime("%d/%m/%Y")
        params = {
            "fly_from" : IATA_from,
            'fly_to' : IATA_to,
            "date_from" : str(tomorrow),
            "date_to" : str(six_months),
            "curr" : "CAD",
            "nights_in_dst_from" : 7,
            "nights_in_dst_to" : 28,
            'flight_type' : 'round',
            'one_for_city' : 1,
            'max_stopovers': 0
        }
        response = requests.get(url=f"{self.base_endpoint}v2/search", params=params, headers=self.headers)
        response.raise_for_status()
        try:
            flight_json = response.json()['data'][0]
            print(f"{city_to} ${flight_json['price']}")
        except IndexError as e:
            print(f"Sorry! No flights found for {city_to}")
            return None
        else:
            price = flight_json['price']
            departure_code = flight_json['route'][0]['flyFrom']
            departure_city = flight_json['route'][0]['cityFrom']
            destination_city = flight_json['route'][0]['cityTo']
            destination_airport = flight_json['route'][0]['flyTo']
            fly_date = flight_json['route'][0]['local_departure'].split('T')[0]
            return_date = flight_json['route'][1]['local_departure'].split('T')[0]
            new_flight = flight_data.FlightData(price, departure_code, departure_city, destination_city, destination_airport, fly_date, return_date)
            self.flights_found.append(new_flight)

        return new_flight