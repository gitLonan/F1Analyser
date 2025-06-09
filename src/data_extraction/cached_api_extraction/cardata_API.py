# other imports
import json
import polars as pl


class CarData:


    @staticmethod
    def get_df_cardata(drivers: list[dict], setparam: object) -> pl.DataFrame:
        list_df_cardata = []
        for driver in drivers:
            print(driver)
            dir_path_content = f"data/cached_calls/car_data/{setparam.session_key}/driver_number_{driver['number']}.json"
            with open(dir_path_content, "r") as file:
                print("Selected drivers: ", driver)
                _ = json.load(file)
                cardata = pl.DataFrame(_)
                list_df_cardata.append(cardata)
        
        return list_df_cardata