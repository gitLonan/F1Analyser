# my imports

# other imports
import json
import polars as pl


class DriversApi:


    @staticmethod
    def set_race_drivers(Setparam: object) -> json:
        """
            Args:
                Setparam (:obj:) - class instance of SetParam
            Sets parameters inside Setparam to be used through out the code
        """
        dir_path_content = f"data/cached_calls/drivers/session_{Setparam.session_key}_drivers.json"
        drivers_list = []
        drivers_number_list = []
        with open(dir_path_content, "r") as file:
            tracks_json = json.load(file)
            for dic in tracks_json: 
               drivers_list.append({f"name":dic["full_name"], "number":dic["driver_number"], "team_name": dic["team_name"]})
               drivers_number_list.append(dic["driver_number"])
            Setparam.list_driver_numbers = drivers_number_list
            Setparam.drivers = drivers_list
        return drivers_list
    
    @staticmethod
    def get_df_drivers(setparam: object) -> pl.DataFrame:
        drivers_df = pl.DataFrame(setparam.drivers)
        return drivers_df
