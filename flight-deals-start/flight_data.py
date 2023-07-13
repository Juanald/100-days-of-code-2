class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, departure_code, departure_city, destination_city, destination_airport, fly_date, return_date) -> None:
        self.price = price
        self.departure_airport_code = departure_code
        self.departure_city = departure_city
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.fly_date = fly_date
        self.return_date = return_date
    
    def __str__(self) -> str:
        return f"""Departure city: {self.departure_city}\nDeparture Code: {self.departure_airport_code}\nDestination City: {self.destination_city}\nDestination Airport: {self.destination_airport}\nFly Date : {self.fly_date}\nReturn Date: {self.return_date}\nPrice: £{self.price}"""