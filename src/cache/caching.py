import json
from src.data_extraction.jsonhandling import JsonHandling
import os
import re

class CacheAPI:
    def cache_tracks(json_data: json, year) -> None:
        with open(f"data/cached_calls/tracks/year_{year}_tracks.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)
            
    def cache_tracks_data(json_data: json, meeting_key) -> None:
        with open(f"data/cached_calls/sessions/meeting_{meeting_key}_tracks_data.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)

    def cache_drivers(json_data: json, session_key) -> None:
        with open(f"data/cached_calls/drivers/session_{session_key}_drivers.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)

    def cache_stints(json_data: json, session_key, driver) -> None:
        with open(f"data/cached_calls/stints/{session_key}/driver_number_{driver}.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)
            
    def cache_laps_data(json_data: json, session_key, driver) -> None:
        with open(f"data/cached_calls/laps/{session_key}/driver_number_{driver}.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)
            
    def cache_car_data(json_data: json, session_key, driver) -> None:
        with open(f"data/cached_calls/car_data/{session_key}/driver_number_{driver}.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)

    def cache_positions(json_data: json, session_key, driver) -> None:
        with open(f"data/cached_calls/positions/{session_key}/drivers_position_{driver}.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)
    
    def exists_data(parmeter: str, folder: str) -> bool:
        """Returns true if the data exists"""
        dir_path_content = f"data/cached_calls/{folder}"
        print(dir_path_content)
        print(folder)
        try:
            list_of_files = os.listdir(dir_path_content)
            print(list_of_files)
        except FileNotFoundError:
            os.makedirs((f"data/cached_calls/{folder}"), exist_ok=True)

        list_of_files = os.listdir(dir_path_content)

        print(list_of_files)
        for file in list_of_files:
            print(file, parmeter)
            match = re.search(f"{parmeter}", file)
            if match:
                print("WE have that file", match[0])
                return True
        print("We dont have that file")
        return False
    
    # def exists_parent_folder(folder: str, amount: int) -> bool:
    #     """
    #         Args: 
    #             folder (str) - name of the 'parent' folder which holds relevant session keys
    #         Returns:
    #             returns bool where false means folder didnt exist and that it created it
    #     """
    #     folder_path = f"data/cached_calls/{folder}"
    #     list_of_files = os.listdir(folder_path)

    #     if not os.path.isdir(folder_path) or len(list_of_files) < 20:
    #         os.makedirs((f"data/cached_calls/{folder}"), exist_ok=True)
    #         return False
    #     return True