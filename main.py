#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
data = DataManager('https://api.sheety.co/21d95537cb39f8e2e273584f8133a12c/copyOfFlightDeals/prices')
flight = FlightSearch()

ORIGIN_CITY_IATA = "LON"
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30)) #* search flights upto this date 

sheetData = data.populateIATA()

for i in sheetData:
    flight.checkFlights(ORIGIN_CITY_IATA, i['iataCode'], from_time=tomorrow, to_time=six_month_from_today)