from src.network.api import ApiCommunication, API, JsonHandling

import json








def main():
    host = 'api.openf1.org'

    data_drivers = ApiCommunication.get_api(host, API.DRIVERS.value, attributes=['session_key=latest', "broadcast_name=O BEARMAN"])
    json_part = JsonHandling.extractingJson(data_drivers)

    data_laps = ApiCommunication.get_api(host, API.LAPS.value, attributes=['driver_number=44', "session_key=latest"])
    json_part = JsonHandling.extractingJson(data_laps)
    #.pretty_json(json_part)

    data_position = ApiCommunication.get_api(host, API.POSITION.value, attributes=['driver_number=44', "session_key=latest"])
    json_part = JsonHandling.extractingJson(data_position)
    #JsonHandling.pretty_json(json_part)

    data_position = ApiCommunication.get_api(host, API.STINTS.value, attributes=['driver_number=44', "session_key=latest"])
    json_part = JsonHandling.extractingJson(data_position)
    JsonHandling.pretty_json(json_part)

    # for num,i in enumerate(json_part[:], start=1):
    #     print(f"Lap: {num}", i["duration_sector_1"], i["duration_sector_2"], i["duration_sector_3"], i['lap_duration'])
  







if __name__ == "__main__":

    main()
