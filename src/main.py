## my Class import
from src.network.api import ApiCommunication, API
from src.DataExtraction.jsonhandling import JsonHandling
from src.cache.caching import CacheAPI
from src.DataExtraction.api.meetingsAPI import MeetingApi

## my Func import

import time
import json








def main():
    host = 'api.openf1.org'

    # data_drivers = ApiCommunication.drivers_api(host, API.DRIVERS.value, attr=[])
    # #data_frame = get_last_race_drivers(data_drivers)
    
    # data_laps = ApiCommunication.get_api(host, API.LAPS.value, attributes=['driver_number=44', "session_key=latest"])
    # json_part = JsonHandling.extracting_json(data_laps)
    # #.pretty_json(json_part)

    # data_position = ApiCommunication.get_api(host, API.POSITION.value, attributes=['driver_number=44', "session_key=latest"])
    # json_part = JsonHandling.extracting_json(data_position)
    # #JsonHandling.pretty_json(json_part)

    # data_position = ApiCommunication.get_api(host, API.STINTS.value, attributes=['driver_number=44', "session_key=latest"])
    # json_part = JsonHandling.extracting_json(data_position)
    # JsonHandling.pretty_json(json_part)

    # json_part = ApiCommunication.get_api(host, API.MEETINGS.value, attr=['year=2024'])
    # print(json_part)
    # tracks = MeetingApi.extract_tracks(json_part)
    # track_data = MeetingApi.extract_tracks_data(json_part)
    # print(JsonHandling.pretty_json(track_data))
    # print(JsonHandling.pretty_json(tracks))
    # CacheAPI.cache_tracks(tracks)
    # CacheAPI.cache_tracks_data(track_data)

    #DA PROBAM SVOJ PLAN

    ##lista trka u zavisnosti od godine
    year = "year=2024"
    json_part = ApiCommunication.get_api(host, API.MEETINGS.value, attr=[year])
    tracks = MeetingApi.extract_tracks(json_part)
    CacheAPI.cache_tracks(tracks)
    print(JsonHandling.pretty_json(json_part))
    #time.sleep(0.2)
    ## izabrao trku
    meeting_key = "meeting_key=1229" #izabrao trku
    json_part = ApiCommunication.get_api(host, API.SESSIONS.value, attr=[year, meeting_key])
    print("-------------------------------")
    print(JsonHandling.pretty_json(json_part))
    #time.sleep(0.2)
    ## izabrao sesiju i 
    session_name = "session_name=Qualifying"
    session_key = "session_key=9472"
    driver_number = "driver_number=44"
    json_part = ApiCommunication.get_api(host, API.STINTS.value, attr=[session_key, driver_number])
    print("-------------------------------")
    time.sleep(0.2)
    ## pre backed analize ili specificne stvari vezano za vozace ili nesto slicno ? 
    session_name = "session_name=Qualifying"
    session_key = "session_key=9468"
    print(JsonHandling.pretty_json(json_part))
    json_part = ApiCommunication.get_api(host, API.LAPS.value, attr=[session_key, driver_number])
    print("-------------------------------")
    print(JsonHandling.pretty_json(json_part))

    

    # for num,i in enumerate(json_part[:], start=1):
    #     print(f"Lap: {num}", i["duration_sector_1"], i["duration_sector_2"], i["duration_sector_3"], i['lap_duration'])
  







if __name__ == "__main__":

    main()
