import time
start = time.time()
## my Class import
from src.network.api_connector import ApiCommunication, API
from src.data_extraction.jsonhandling import JsonHandling
from src.data_extraction.cached_api_extraction.meetings_API import MeetingApi
from src.data_extraction.cached_api_extraction.drivers_API import DriversApi
from src.data_extraction.cached_api_extraction.laps_API import Laps
from src.cache.caching import CacheAPI
from src.analysis.uttility import SetParam
from src.sim_gui import SimulateGui
from src.analysis.analysis import Analysis

## my Func import


import time
import os
import sys


after_importing = time.time()
print("Time it took to load imports: ", after_importing-start)


def main():
    host = 'api.openf1.org'
    Setparam = SetParam()

    year, year_attr = SimulateGui.get_year_input()
    if not CacheAPI.exists_data(year, "tracks"):  
        print("We dont have data for that year")
        json_part = ApiCommunication.get_api(host, API.MEETINGS.value, attr=[year_attr])
        CacheAPI.cache_tracks(json_part, year)
    track_list = MeetingApi.extract_tracks(year, Setparam)
    SimulateGui.show_tracks(track_list)
    meeting_key = SimulateGui.get_meeting_key(Setparam)


    if not CacheAPI.exists_data(Setparam.meeting_key, "sessions"):
        print("We dont have data for that track")
        json_part = ApiCommunication.get_api(host, API.SESSIONS.value, attr=[meeting_key])
        CacheAPI.cache_tracks_data(json_part, Setparam.meeting_key)
    session_list = MeetingApi.extract_track_sessions(year, Setparam)
    SimulateGui.show_sessions(session_list)
    session_key = SimulateGui.get_session_key(Setparam)

    if not CacheAPI.exists_data(Setparam.session_key, "drivers"):
        json_part = ApiCommunication.get_api(host, API.DRIVERS.value, attr=[f"session_key={Setparam.session_key}"])
        CacheAPI.cache_drivers(json_part, Setparam.session_key)
        print(JsonHandling.pretty_json(json_part))
    drivers = DriversApi.get_race_drivers(Setparam) 
    print(drivers)
    SimulateGui.show_drivers(drivers)
    
    if not CacheAPI.exists_data(Setparam.session_key, f"stints"):
        os.makedirs((f"data/cached_calls/stints/{Setparam.session_key}"), exist_ok=True)
        for num in Setparam.list_driver_numbers:
            time.sleep(0.5)
            if not CacheAPI.exists_data(num, f"stints/{Setparam.session_key}") or not len(os.listdir(f"data/cached_calls/stints/{Setparam.session_key}")) == 20:
                json_part = ApiCommunication.get_api(host, API.STINTS.value, attr=[f"session_key={Setparam.session_key}", f"driver_number={num}"])
                pretty_json = JsonHandling.pretty_json(json_part)
                CacheAPI.cache_stints(json_part, Setparam.session_key, num)

    if not CacheAPI.exists_data(SetParam.session_key, "laps"):
        os.makedirs((f"data/cached_calls/laps/{Setparam.session_key}"), exist_ok=True)
        for num in Setparam.list_driver_numbers:
            time.sleep(0.5)
            if not CacheAPI.exists_data(num, f"laps/{Setparam.session_key}") or not len(os.listdir(f"data/cached_calls/laps/{Setparam.session_key}")) == 20:
                json_part = ApiCommunication.get_api(host, API.LAPS.value, attr=[f"session_key={Setparam.session_key}", f"driver_number={num}"])
                #pretty_json = JsonHandling.pretty_json(json_part)
                CacheAPI.cache_laps_data(json_part, Setparam.session_key, num)


    SimulateGui.show_analysis_option()
    while True:
        if SimulateGui.choose_analysis() == 1:
            race = Analysis(Setparam.session_key, Setparam.meeting_key)
            print("Plotting session stints...")
            race.stints(Setparam)
            print("Stints ploted")
        elif SimulateGui.choose_analysis() == 2:
            race = Analysis(Setparam.session_key, Setparam.meeting_key)
            Laps.get_single_df_laps(Setparam.session_key, 1)
            race.drivers_lap_time(Setparam, 1)
        elif SimulateGui.choose_analysis() == 0:
            sys.exit()




if __name__ == "__main__":
    end = time.time()

    main()
