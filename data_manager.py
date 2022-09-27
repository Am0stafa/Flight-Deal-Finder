import requests
from flight_search import FlightSearch
    
class DataManager:
    def __init__(self,api):
        self.api = api
        self.sheetData = {}
        
    def populateIATA(self):
        x = requests.get(self.api)
        self.sheetData  = x.json()["prices"]
        flightSearch = FlightSearch()
        for i in self.sheetData:
            if len(i["iataCode"]) == 0:
                iata = flightSearch.getDestinationCode(i["city"])
                i["iataCode"] = iata
                id = i["id"]
                url = f"https://api.sheety.co/21d95537cb39f8e2e273584f8133a12c/copyOfFlightDeals/prices/{id}"
                requests.put(url, data = i)
                new_data = {
                    "price": {
                        "iataCode": i["iataCode"]
                    }
                }
                response = requests.put(
                    url=url,
                    json=new_data
                )

                    
                
        return self.sheetData         