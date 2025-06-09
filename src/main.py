import time
start = time.time()
## my Class import
from src.web_request.api_connector import ApiCommunication, API
from src.data_extraction.jsonhandling import JsonHandling
from src.data_extraction.cached_api_extraction.meetings_API import MeetingApi
from src.data_extraction.cached_api_extraction.drivers_API import DriversApi
from src.data_extraction.cached_api_extraction.laps_API import LapsAPI
from src.cache.caching import CacheAPI
from src.analysis.uttility import SetParam
from src.sim_gui import SimulateGui
from src.analysis.analysis import Analysis, Race
from src.analysis.ploting import PlotingAnalysis


## my Func import


import time
import os
import sys
from datetime import datetime



after_importing = time.time()
print("Time it took to load imports: ", after_importing-start)



def main():
    host = 'api.openf1.org'
    setparam = SetParam()
    current_year = datetime.now().year

    year, year_attr = SimulateGui.get_year_input(setparam)
    print(type(year), type(current_year), year_attr)
    if setparam.call_again == True:
        print("USAO", year, year_attr)
        json_part = ApiCommunication.get_api(host, API.MEETINGS.value, attr=[year_attr])
        CacheAPI.cache_tracks(json_part, year)
    elif not CacheAPI.exists_data(year, "tracks"):  
        print("We dont have data for that year")
        json_part = ApiCommunication.get_api(host, API.MEETINGS.value, attr=[year_attr])
        CacheAPI.cache_tracks(json_part, year)
    track_list = MeetingApi.set_meeting_keys(year, setparam)
    SimulateGui.show_tracks(track_list)
    meeting_key = SimulateGui.get_meeting_key(setparam)


    if not CacheAPI.exists_data(setparam.meeting_key, "sessions"):
        print("We dont have data for that track")
        json_part = ApiCommunication.get_api(host, API.SESSIONS.value, attr=[setparam.meeting_key_attr])
        CacheAPI.cache_tracks_data(json_part, setparam.meeting_key)
    session_list = MeetingApi.set_session_keys(year, setparam)
    SimulateGui.show_sessions(session_list)
    session_key = SimulateGui.get_session_key(setparam)

    if not CacheAPI.exists_data(setparam.session_key, "drivers"):
        json_part = ApiCommunication.get_api(host, API.DRIVERS.value, attr=[setparam.session_key_attr])
        CacheAPI.cache_drivers(json_part, setparam.session_key)
        print(JsonHandling.pretty_json(json_part))
    drivers = DriversApi.set_race_drivers(setparam) 
    print(setparam.drivers)
    SimulateGui.show_drivers(setparam.drivers)
    
    if not CacheAPI.exists_data(setparam.session_key, f"stints"):
       #os.makedirs((f"data/cached_calls/stints/{setparam.session_key}"), exist_ok=True)
        
        for num in setparam.list_driver_numbers:
            # response = requests.get(f"https://api.openf1.org/v1/stints?session_key={setparam.session_key}&driver_number={num}")
            # print(response.json())
            
            if not CacheAPI.exists_data(num, f"stints/{setparam.session_key}"):
                json_part = ApiCommunication.get_api(host, API.STINTS.value, attr=[f"session_key={setparam.session_key}", f"driver_number={num}"])
                pretty_json = JsonHandling.pretty_json(json_part)
                CacheAPI.cache_stints(json_part, setparam.session_key, num)
    print("OVO GLEDAJ", JsonHandling.pretty_json(setparam.drivers))

    if not CacheAPI.exists_data(setparam.session_key, "laps"):
        os.makedirs((f"data/cached_calls/laps/{setparam.session_key}"), exist_ok=True)

        for num in setparam.list_driver_numbers:
            time.sleep(0.2)
            if not CacheAPI.exists_data(num, f"laps/{setparam.session_key}"):
                json_part = ApiCommunication.get_api(host, API.LAPS.value, attr=[f"session_key={setparam.session_key}", f"driver_number={num}"])
                if len(json_part) == 0:
                    print("No LAP data for that driver")
                    continue
                pretty_json = JsonHandling.pretty_json(json_part)
                CacheAPI.cache_laps_data(json_part, setparam.session_key, num)
    
    if not CacheAPI.exists_data(setparam.session_key, "positions"):
        os.makedirs((f"data/cached_calls/positions/{setparam.session_key}"), exist_ok=True)

        for num in setparam.list_driver_numbers:
            time.sleep(0.2)
            if not CacheAPI.exists_data(num, f"positions/{setparam.session_key}"):
                json_part = ApiCommunication.get_api(host, API.POSITION.value, attr=[f"session_key={setparam.session_key}", f"driver_number={num}"])
                if len(json_part) == 0:
                    print("No Position data for that driver")
                    continue
                CacheAPI.cache_positions(json_part, setparam.session_key, num)



    SimulateGui.show_analysis_option()
    while True:
        os.makedirs((f"data/images_for_sending"), exist_ok=True)
        key = SimulateGui.choose_analysis()
        #Stints duration for all drivers
        if  key == 1:
            analysis = Analysis(setparam.session_key, setparam.meeting_key)
            print("Plotting session stints...")
            df_stints = analysis.stints(setparam)
            PlotingAnalysis.plot_stints(df_stints)
            print("Stints ploted")
        
        #Fastest sectors and fastest lap time
        elif key == 2:
            race = Race(setparam.session_key, setparam.meeting_key)
            df_average_for_stints = race.all_drivers_average_times_per_stint(setparam)
            print("PLotting average times for secotr and laps for stints....")
            PlotingAnalysis.plot_average_for_stints(df_average_for_stints)
            print("Plotted average times")

        #Average sectors and lap time for stints
        elif key == 3:
            analysis = Analysis(setparam.session_key, setparam.meeting_key)
            print("PLotting fastest sectors....")
            df_fastest_sectors = analysis.all_drivers_fastest_sectors(setparam)
            PlotingAnalysis.plot_fastest_secotors(df_fastest_sectors)
            print("Fastest sectors plotted")
        
        #Car data
        elif key == 4:
            analysis = Analysis(setparam.session_key, setparam.meeting_key)
            SimulateGui.show_drivers(setparam.drivers)

            SimulateGui.choose_drivers_for_car_data(setparam)
            

            if not CacheAPI.exists_data(setparam.session_key, "car_data"):
                 os.makedirs((f"data/cached_calls/car_data/{setparam.session_key}"), exist_ok=True)
                 for num in setparam.index_for_selecting_drivers:
                    time.sleep(0.1)
                    if not CacheAPI.exists_data(setparam.list_driver_numbers[num], f"car_data/{setparam.session_key}/driver_number_{setparam.list_driver_numbers[num]}"):
                        json_part = ApiCommunication.get_api(host, API.CARDATA.value, attr=[f"session_key={setparam.session_key}", f"driver_number={setparam.list_driver_numbers[num]}"])
                        if len(json_part) == 0:
                            print("No LAP data for that driver")
                            continue
                        CacheAPI.cache_car_data(json_part, setparam.session_key, drivers[num])

            drivers = [setparam.drivers[num] for num in setparam.index_for_selecting_drivers]
            print("These are selected drivers", drivers)
            df_speed_data, df_list_lap_number_and_start_date = analysis.car_data(drivers, setparam)
            PlotingAnalysis.plot_car_data(df_speed_data, df_list_lap_number_and_start_date)

        elif key == 5:
            race = Race(setparam.session_key, setparam.meeting_key)
            SimulateGui.show_drivers(setparam.drivers)
            SimulateGui.choose_drivers_for_car_data(setparam)
        
            if not CacheAPI.exists_data(setparam.session_key, "location"):
                os.makedirs((f"data/cached_calls/location/{setparam.session_key}"), exist_ok=True)
                for num in setparam.index_for_selecting_drivers:
                    time.sleep(0.1)
                    if not CacheAPI.exists_data(setparam.list_driver_numbers[num], f"location/{setparam.session_key}/drivers_location_{setparam.list_driver_numbers[num]}"):
                        json_part = ApiCommunication.get_api(host, API.LOCATION.value, attr=[f"session_key={setparam.session_key}", f"driver_number={setparam.list_driver_numbers[num]}"])
                        if len(json_part) == 0:
                            print(f"No Location data for {setparam.list_driver_numbers[num]}")
                            continue
                        CacheAPI.cache_car_location(json_part, setparam.session_key, setparam.list_driver_numbers[num])
                






        elif key == 0:
            sys.exit()




if __name__ == "__main__":
    end = time.time()

    main()
