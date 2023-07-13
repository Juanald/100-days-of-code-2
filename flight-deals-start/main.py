#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager, flight_search, notification_manager
from pprint import pprint

ORIGIN_CITY_IATA = "YYZ"
SHEET_DATA = [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 2000, 'id': 2}, {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 42, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 485, 'id': 4}, {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 551, 'id': 5}, {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 95, 'id': 6}, {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 414, 'id': 7}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 240, 'id': 8}, {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 260, 'id': 9}, {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 378, 'id': 10}]

datamanager = data_manager.DataManager()
flight_searcher = flight_search.FlightSearch()
telegram_bot = notification_manager.NotificationManager()

def pop_IATA(sheet_data):
    # Call this function if you want to populate IATA codes within the sheet
    for data in sheet_data:
        if len(data['iataCode']) == 0:
            data['iataCode'] = flight_searcher.give_IATA(data['city'])
            datamanager.post_data(data['id'], {"price" : data })


def main():
    for data in SHEET_DATA:
        flight = flight_searcher.find_flights(ORIGIN_CITY_IATA, data['iataCode'], data['city'])
        try:
            print(f"{data['city']}: ${flight.price}")
        except AttributeError:
            continue
        if flight.price < data['lowestPrice']:
            message = f"""Low price alert! Only ${flight.price} to fly from {flight.departure_city}-{flight.departure_airport_code} to {flight.destination_city}-{flight.destination_airport} from {flight.fly_date} to {flight.return_date}!"""
            telegram_bot.send_message(message)

if __name__ == "__main__":
    main()