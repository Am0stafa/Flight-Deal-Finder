import requests

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "-pIBIVEFvEJOCrtHA190XzSEF0WQQcio"
from flight_data import FlightData
from notification_manager import NotificationManager

class FlightSearch:
    def __init__(self):
        self.notification = NotificationManager()
        
    def getDestinationCode(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code
        
    #^ A single flights search.
    #* automatically search all the flight in  this data rage and return the cheapest one
    def checkFlights(self, origin_city_code, destination_city_code, from_time, to_time,cheapest):
        """
         we're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6x30days) time. We're also looking for round trips that return between 7 and 28 days in length. The currency of the price we get back should be in GBP.
        """
    
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )
        data = response.json()["data"]
        
        if len(data) == 0:
            print("no flights")
            return None
            

        
        data = data[0]
        
        
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        if flight_data.price < cheapest:
            self.notification.sendSMS(flight_data.getMessage())
            print("deal found")
            
        
        return flight_data
        