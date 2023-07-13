#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager, flight_search, notification_manager
from pprint import pprint

ORIGIN_CITY_IATA = "YYZ"

datamanager = data_manager.DataManager()
flight_searcher = flight_search.FlightSearch()
telegram_bot = notification_manager.NotificationManager()

def pop_IATA(sheet_data):
    for data in sheet_data:
        if len(data['iataCode']) == 0:
            data['iataCode'] = flight_searcher.give_IATA(data['city'])
            datamanager.post_data(data['id'], {"price" : data })


def main():
    
    sheet_data = datamanager.get_data()
    pop_IATA(sheet_data)
    for data in sheet_data:
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