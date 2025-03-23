from src.network.api import ApiCommunication, API

import json








def main():
    host = 'api.openf1.org'
    print("GLEDAJ", API.DRIVERS.value)
    data = ApiCommunication.get_api(host, API.DRIVERS.value, attributes=['session_key=latest', "broadcast_name=O BEARMAN"])
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAaa", data)
    json_part = ApiCommunication.extractingJson(data)
    data = ApiCommunication.get_api(host, API.LAPS.value, attributes=['driver_number=44', "session_key=latest"])
    json_part = ApiCommunication.extractingJson(data)
    #print(json_part)
    for num,i in enumerate(json_part[:], start=1):
        print(f"Lap: {num}", i["duration_sector_1"], i["duration_sector_2"], i["duration_sector_3"], i['lap_duration'])
  







if __name__ == "__main__":

    main()
